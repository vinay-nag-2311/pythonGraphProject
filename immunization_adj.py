class Vertex:
    def __init__(self, vtx_name: str, vtx_type: str):
        self.name = vtx_name
        self.type = vtx_type
        self.adjacent = []

    def __eq__(self, other):
        if isinstance(other, Vertex):
            return self.name == other.name and \
                   self.type == other.type
        return False

    def __str__(self):
        return str(self.name) + ' connected to ' + \
               str([x.type + ": " + x.name for x in self.adjacent])

    def add_connection(self, conn):
        if conn not in self.adjacent:
            self.adjacent.append(conn)

    def get_connections(self):
        return self.adjacent


class Immunization:
    def __init__(self):
        self.vertex_list = []

    def __iter__(self):
        return iter(self.vertex_list)

    def __getitem__(self, name):
        try:
            v = [s for s in self.vertex_list if s.name == name][0]
            return v
        except ValueError:
            print("Vertex with name :"+name+" not found!!")

    def add_vertex(self, vtx_name, vtx_type):
        new_vertex = Vertex(vtx_name, vtx_type)
        if new_vertex not in self.vertex_list:
            self.vertex_list.append(new_vertex)

    def is_vertex_present(self, v):
        return v in self.vertex_list

    def list_connections(self, v):
        list_conn = [ve for s in self.vertex_list if s == v
                     for ve in s.get_connections()]
        return list_conn

    def add_edge(self, strn, vacc):
        """ """

        str_vertex = Vertex(strn, 'strain')
        vacc_vertex = Vertex(vacc, 'vaccine')

        if not self.is_vertex_present(str_vertex):
            self.add_vertex(str_vertex, 'strain')
        if not self.is_vertex_present(vacc_vertex):
            self.add_vertex(vacc_vertex, 'vaccine')

        self[str_vertex.name].add_connection(vacc_vertex)
        self[vacc_vertex.name].add_connection(str_vertex)

    def readInputFile(self, input_file):
        """ """
        with open(input_file, 'r') as f:
            input_file_read = f.read()
        input_split = input_file_read.split("\n")
        for i in input_split:
            each_split = i.replace("/", " ").split()
            self.add_vertex(each_split[0], 'strain')
            for j in range(1, len(each_split)):
                self.add_vertex(each_split[j], 'vaccine')
                self.add_edge(each_split[0], each_split[j])
        return self

    def displayAll(self):
        """This function displays the total number (count) of unique
         vaccines and strains entered through the input file.
         It should also list out the unique vaccines and strains.
         The output of this function should be pushed into outputPS16.txt file.
         The output format should be as mentioned below.
         """
        strn_list = [x for x in self.vertex_list if x.type == "strain"]
        vacc_list = [x for x in self.vertex_list if x.type == "vaccine"]
        func_intro = "\n--------Function displayAll--------"
        num_strains = "\nTotal no. of strains: " + \
                      str(len(strn_list))
        num_vaccines = "\nTotal no. of vaccines: " + \
                       str(len(vacc_list))
        list_strains = "\nList of strains:"
        for s in strn_list:
            list_strains += ("\n" + s.name)
        list_vaccines = "\n\nList of vaccines:"
        for v in vacc_list:
            list_vaccines += ("\n" + v.name)
        func_end = "\n" + "-" * 16 + "\n"
        print(func_intro, num_strains, num_vaccines,
              list_strains, list_vaccines, func_end)
        # with open("outputPS16.txt", "a") as fout:
        #     fout.write(func_intro + num_strains + num_vaccines +
        #                list_strains + list_vaccines + func_end)
        #     fout.close()

    def displayStrains(self, vaccine):
        output_intro_str = """--------Function displayStrain --------\n"""
        vacc = Vertex(vaccine, 'vaccine')
        if vacc in self.vertex_list:
            list_strains = [v.name for v in self[vaccine].get_connections()]
            vaccine_info = "Vaccine name: " + vaccine + "\n" + \
                           "List of Strains:\n"
            if len(list_strains) > 0:
                strain_print = "\n".join(list_strains)
            else:
                strain_print = "***There are no strains on which " + vaccine + " is effective.***"
            output_info = vaccine_info + strain_print
        else:
            output_info = "***Information about " + vaccine + " is not available.***"
        print(output_intro_str, output_info)
        # with open("outputPS16.txt", "a") as fout:
        #     fout.write(output_intro_str + output_info)
        #     fout.close()

    def displayVaccine(self, strain):
        """ """
        output_intro_str = """--------Function displayVaccine --------\n"""
        strn = Vertex(strain, 'strain')
        if strn in self.vertex_list:
            list_vaccines = [v.name for v in self[strain].get_connections()]
            strain_info = "Strain name: " + strain + "\n" + \
                          "List of Vaccines:\n"
            if len(list_vaccines) > 0:
                vaccine_print = "\n".join(list_vaccines)
            else:
                vaccine_print = "***There are no vaccines which are effective on " + strain + ".***"
            output_info = strain_info + vaccine_print
        else:
            output_info = "***Information about " + strain + " is not available.***"
        print(output_intro_str, output_info)
        # with open("outputPS16.txt", "a") as fout:
        #     fout.write(output_intro_str + output_info)
        #     fout.close()

    def dfs(self, strt):
        """Do a depth-first search of the graph, from the start node.
        Return a list of nodes in visited order, the first being start.
        Assume the start node exists.
        """
        start = Vertex(strt, 'vaccine')
        visited = []
        to_visit = [start]
        while to_visit:
            next_node = to_visit.pop()
            visited.append(next_node)
            print(self[next_node.name])
            for conn in self.list_connections(next_node):
                if conn not in visited and conn not in to_visit:
                    to_visit.append(conn)
        return visited

    def bfs(self, strt):
        """Do a breadth-first search of the graph, from the start node.
        Return a list of nodes in visited order, the first being start.
        Assume the start node exists.
        """
        start = Vertex(strt, 'vaccine')
        visited = []
        to_visit = [start]
        while to_visit:
            next_node = to_visit.pop(0)
            visited.append(next_node)
            print(self[next_node.name])
            for conn in self.list_connections(next_node):
                if conn not in visited and conn not in to_visit:
                    to_visit.append(conn)
        return visited

    def commonStrain(self, vacA, vacB):
        """ """
        strA = self.list_connections(Vertex(vacA, 'vaccine'))
        strB = self.list_connections(Vertex(vacB, 'vaccine'))

        output_intro = f"""--------Function commonStrain --------
Vaccine A: {vacA}
Vaccine B: {vacB}
Common Strain: """
        output_info = []
        for x in strA:
            if x in strB:
                output_info.append(x.name)
        if len(output_info) > 0:
            output_info = "Yes, " + ", ".join(output_info)
        else:
            output_info = "***There are no common strains between the above 2 vaccines.***"
        print(output_intro + output_info)
        # with open("outputPS16.txt", "a") as fout:
        #     fout.write(output_intro + output_info)
        #     fout.close()

    def findVaccineConnect(self, vacA, vacB):
        return None


if __name__ == '__main__':
    g = Immunization()
    file_path = 'inputPS16.txt'
    g.readInputFile(file_path)
    g.displayAll()
    # for a in g:
    #     print(a)
    # g.displayStrains('Covaxin')
    # g.displayVaccine('B117')
    # g.commonStrain('Covaxin', 'CoviShield')

    # for i in g.dfs('Covaxin'):
    #     print(i)
    # for i in g.dfs('Covaxin'):
    #     print(i)
