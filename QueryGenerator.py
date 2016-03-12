from Repository import Repository
from DomainModel.Query import Query

class QueryGenerator:

    def __init__(self, repository):
        self.repo = repository

    def generate_query(self, query_name):
        queries = self.repo.retrieve_query_with_dependencies(query_name)
        if len(queries) == 1:
            return queries[0].text

        output = "with "
        for item in queries[:-1]:
            output += "{0} as ({1}),".format(item.name, item.text)
        output = output[:-1]
        output += queries[-1].text
        return output

class TestQueryGenerator:

    def __init__(self, repo: Repository, node_name: str, simulated_nodes: list, test_id: int):
        self.repo = repo
        self.node_name = node_name
        self.simulated_nodes = simulated_nodes
        self.test_id = test_id

    def get_dependency_graph(self, query, simulated_nodes):
        output = []
        newDeps = query.dependencies
        while len(newDeps) != 0:
            dependentQueries = [self.repo.retrieve_query(x) for x in newDeps]
            output.extend(dependentQueries)
            newDepsNonFlat = [x.dependencies for x in dependentQueries if x.name not in simulated_nodes]
            newDeps = [item for sublist in newDepsNonFlat for item in sublist]
        final_output = []
        for queryName in output[::-1]:
            if queryName not in final_output:
                final_output.append(queryName)
        return final_output

    def generate(self):

        node = self.repo.retrieve_query(self.node_name)

        if node.dependencies == []:
            return node.query["string"]

        dep_graph = self.get_dependency_graph(node, self.simulated_nodes)
        output = "with "
        for query in dep_graph:
            if query.name in self.simulated_nodes:
                output += "{0} as ( select * from tests.{0} where test_id = {1} ),".format(query.name, str(self.test_id))
            else:
                output += "{0} as ({1}),".format(query.name, query.query["string"])
        output = output[:-1]
        output += " " + node.query["string"]
        return output