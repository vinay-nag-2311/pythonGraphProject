class Vertex:
    """
    Class to define a vertex in our graph.
    Here, a vertex signifies a Vaccine or Strain.
    """
    def __init__(self, vtx_name: str, vtx_type: str):
        """Initialise an empty vertex."""
        self.name = vtx_name
        self.type = vtx_type

    def __eq__(self, other):
        if isinstance(other, Vertex):
            return self.name == other.name and \
                   self.type == other.type
        return False

    def __str__(self):
        return str(self.type + " : " + self.name)


class Immunization:
    """
    Class to define the graph of vaccines and strains.
    Initialised using 2 components :
    vaccine_list - Stores vaccines and strains
                   as a list of Vertex.
    edges - Stores the list of (vaccine, strain)
            combinations representing the edges
            of the graph.
    """

    def __init__(self):
        """Initialise an empty graph."""
        self.vaccine_list = list()
        self.edges = list()

    def __iter__(self):
        return iter(self.vaccine_list)

    def __contains__(self, vertex: Vertex):
        return vertex in self.vaccine_list

    def is_empty(self):
        """Check if graph is empty."""
        return len(self.vaccine_list) == 0

    def readInputfile(self, input_file):
        """
        This function reads the input file inputPS16.txt
        containing the name of the strains and associated
        vaccines in one line.
        :param input_file: path of input file.
        """
        with open(input_file, 'r') as fi:
            input_file_read = fi.read()
        input_split = input_file_read.split("\n")

        # loop across the lines of the file
        for i in input_split:
            each_split = i.replace("/", " ").split()
            s = Vertex(each_split[0], 'strain')
            self.add_vertex(s)
            if len(i) > 2:
                for j in range(1, len(each_split)):
                    v = Vertex(each_split[j], 'vaccine')
                    self.add_vertex(v)
                    self.add_edge(s, v)

        return self

    def has_vertex(self, node):
        """
        Check if vertex is present in the graph.
        :param node: Vertex to be checked.
        """
        return node in self.vaccine_list

    def has_edge(self, s, v):
        """
        Check if edge is present in the graph.
        :param s: Strain-Vertex name.
        :param v: Vaccine-Vertex name.
        """
        return (
                self.has_vertex(Vertex(s, 'strain')) and
                self.has_vertex(Vertex(v, 'vaccine')) and
                (Vertex(s, 'strain'), Vertex(v, 'vaccine')) in self.edges
        )

    def add_vertex(self, node):
        """
        Add Vertex into the graph.
        :param node: Vertex to be added.
        """
        if not self.has_vertex(node):
            self.vaccine_list.append(node)

    def add_edge(self, str_vertex, vacc_vertex):
        """
        Add edge into the graph.
        :param str_vertex: Strain-Vertex.
        :param vacc_vertex: Vaccine-Vertex.
        """
        if not self.has_vertex(str_vertex):
            self.add_vertex(str_vertex)
        if not self.has_vertex(vacc_vertex):
            self.add_vertex(vacc_vertex)

        self.add_vertex(str_vertex)
        self.add_vertex(vacc_vertex)
        self.edges.append((str_vertex, vacc_vertex))

    def displayAll(self):
        """
        This function displays the total number (count)
        of unique vaccines and strains entered through
        the input file.
        It should also list out the unique vaccines and
        strains.The output of this function should be
        pushed into outputPS16_bkp.txt file.
        The output format should be as mentioned below.
        """
        strn_list = [x for x in self.vaccine_list if x.type == "strain"]
        vacc_list = [x for x in self.vaccine_list if x.type == "vaccine"]
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

        with open("outputPS16_bkp.txt", "a") as fout:
            fout.write(func_intro + num_strains + num_vaccines +
                       list_strains + list_vaccines + func_end)
            fout.close()

    def displayStrains(self, vacc):
        """
        This function displays all the strains a particular
        vaccine is associated with.
        :param vacc: Vaccine-name.
        """
        vaccine = Vertex(vacc, 'vaccine')
        output_intro_str = """\n--------Function displayStrain --------\n"""
        if vaccine in self.vaccine_list:
            list_strains = [conn[0].name for conn in self.edges
                            if (conn[1] == vaccine)]
            vaccine_info = "Vaccine name: " + vacc + "\n" + \
                           "List of Strains:\n"
            if len(list_strains) > 0:
                strain_print = "\n".join(list_strains)
            else:
                strain_print = "***There are no strains on which " + \
                               vacc + " is effective.***"
            output_info = vaccine_info + strain_print
        else:
            output_info = "***Information about '" + vacc + "' is not available.***"

        with open("outputPS16_bkp.txt", "a") as fout:
            fout.write(output_intro_str + output_info)
            fout.close()

    def displayVaccine(self, strn):
        """
        This function displays all the vaccines
        associated with a strain.
        :param strn: Strain-name.
        """
        strain = Vertex(strn, 'strain')
        output_intro_str = """\n--------Function displayVaccine --------\n"""
        if strain in self.vaccine_list:
            list_vaccines = [conn[1].name for conn in self.edges
                             if (conn[0] == strain)]
            strain_info = "Strain name: " + strn + "\n" + \
                          "List of Vaccines:\n"
            if len(list_vaccines) > 0:
                vaccine_print = "\n".join(list_vaccines)
            else:
                vaccine_print = "***There are no vaccines which are " + \
                                "effective on " + strn + ".***"
            output_info = strain_info + vaccine_print
        else:
            output_info = "***Information about '" + strn + "' is not available.***"

        with open("outputPS16_bkp.txt", "a") as fout:
            fout.write(output_intro_str + output_info)
            fout.close()

    def list_connections(self, v):
        """
        List all the edges of the Vertex V.
        :param v: Vertex - can be a vaccine or strain
        """
        if v.type == 'vaccine':
            list_conn = [x[0] for x in self.edges if x[1] == v]
        else:
            list_conn = [x[1] for x in self.edges if x[0] == v]
        return list_conn

    def commonStrain(self, vacA, vacB):
        """
        This function finds out if two vaccine are related
        to each other through one common strain using the
        Breadth-first traversal technique.
        :param vacA: Vaccine-A name
        :param vacB: Vaccine-B name
        """
        output_intro = f"""\n--------Function commonStrain --------
Vaccine A: {vacA}
Vaccine B: {vacB}
Common Strain: """
        output_string = f"***'{vacA}' and '{vacB}' are not related " + \
                        f"to each other through one common strain.***"
        start = Vertex(vacA, 'vaccine')
        end = Vertex(vacB, 'vaccine')

        if not self.has_vertex(start):
            output_string = f"***Information about '{vacA}' " + \
                            "is not available.***"
        elif not self.has_vertex(end):
            output_string = f"***Information about '{vacB}' " + \
                            "is not available.***"
        else:
            visited = []
            to_visit = [[start]]
            if start == end:
                output_string = f"Inputs '{vacA}' and '{vacB}' " + \
                                "refer to the same vaccine."
                with open("outputPS16_bkp.txt", "a") as fout:
                    fout.write(output_intro + output_string)
                    fout.close()
                return
            while to_visit:
                path = to_visit.pop(0)
                node = path[-1]
                if node not in visited:
                    neighbours = self.list_connections(node)
                    for neighbour in neighbours:
                        new_path = list(path)
                        new_path.append(neighbour)
                        to_visit.append(new_path)
                        if neighbour == end and len(new_path) == 3:
                            output_string = "Yes, " + new_path[1].name + "."
                            with open("outputPS16_bkp.txt", "a") as fout:
                                fout.write(output_intro + output_string)
                                fout.close()
                            return
                    visited.append(node)
        with open("outputPS16_bkp.txt", "a") as fout:
            fout.write(output_intro + output_string)
            fout.close()
        return

    def findVaccineConnect(self, vacA, vacB):
        """
        This function finds out if two vaccines A and B are
        related to each other through a common vaccine C
        using the Depth-first traversal technique.
        :param vacA: Vaccine-A name
        :param vacB: Vaccine-B name
        """
        output_intro = f"""\n--------Function findVaccineConnect --------
Vaccine A: {vacA}
Vaccine B: {vacB}
Related: """
        output_string = f"***'{vacA}' and '{vacB}' are not related " + \
                        f"to each other through a common vaccine.***"
        start = Vertex(vacA, 'vaccine')
        end = Vertex(vacB, 'vaccine')

        if not self.has_vertex(start):
            output_string = f"***Information about '{vacA}' " + \
                            f"is not available.***"
        elif not self.has_vertex(end):
            output_string = f"***Information about '{vacB}' " + \
                            f"is not available.***"
        else:
            visited = []
            to_visit = [[start]]
            if start == end:
                output_string = f"Inputs '{vacA}' and '{vacB}' " + \
                                "refer to the same vaccine."
                with open("outputPS16_bkp.txt", "a") as fout:
                    fout.write(output_intro + output_string)
                    fout.close()
                return
            while to_visit:
                path = to_visit.pop(0)
                node = path[-1]
                if node not in visited:
                    neighbours = self.list_connections(node)
                    for neighbour in neighbours:
                        new_path = list(path)
                        new_path.append(neighbour)
                        to_visit.append(new_path)
                        if neighbour == end:
                            if len(new_path) == 5:
                                visited_name = [x.name for x in new_path]
                                output_string = "Yes, " + " > " \
                                    .join(visited_name) + ""
                                with open("outputPS16_bkp.txt", "a") as fout:
                                    fout.write(output_intro + output_string)
                                    fout.close()
                                    return
                            else:
                                with open("outputPS16_bkp.txt", "a") as fout:
                                    fout.write(output_intro + output_string)
                                    fout.close()
                                    return
                    visited.append(node)
        with open("outputPS16_bkp.txt", "a") as fout:
            fout.write(output_intro + output_string)
            fout.close()
        return


if __name__ == '__main__':
    # initialise paths
    file_path = 'inputPS16.txt'
    prompts_path = 'promptsPS16.txt'

    # read input path
    a = Immunization().readInputfile(file_path)
    a.displayAll()

    # prompt path
    with open(prompts_path, 'r') as f:
        file_read = f.read()
    input_spl = file_read.split("\n")

    # run prompts
    for line in input_spl:
        l_arr = line.split(":")
        if l_arr[0] == "displayStrains":
            a.displayStrains(l_arr[1].strip())
        elif l_arr[0] == "listVaccine":
            a.displayVaccine(l_arr[1].strip())
        elif l_arr[0] == "commonStrain":
            a.commonStrain(l_arr[1].strip(),
                           l_arr[2].strip())
        elif l_arr[0] == "findVaccineConnect":
            a.findVaccineConnect(l_arr[1].strip(),
                                 l_arr[2].strip())
        else:
            print("***Prompt : " + l_arr[0] +
                  " - Not implemented!")
