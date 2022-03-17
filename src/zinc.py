from opencmiss.zinc.context import Context
from opencmiss.zinc.region import Region
from opencmiss.zinc.field import Field
from opencmiss.zinc.node import Node
from opencmiss.zinc.status import OK as RESULT_OK
from opencmiss.utils.zinc.general import ChangeManager
from opencmiss.utils.zinc.field import get_group_list


def load(file_path: str, file_name: str) -> dict:
    zinc_context = Context("Digitiser")
    region = zinc_context.getDefaultRegion()
    result = region.readFile(file_path)
    assert result == RESULT_OK, f"Error reading digitised file {file_name}."
    child_region = region.getFirstChild()
    if child_region.isValid():
        return get_groups(child_region)


def get_groups(region: Region) -> dict:
    """ Finds node groups and extracts node coordinates.
    :param region: OpenCMISS-ZINC region where the nodes are stored.
    :return: a dictionary of node values with corresponding class ids.
    """
    field_module = region.getFieldmodule()
    with ChangeManager(field_module):
        field_cache = field_module.createFieldcache()
        coordinate_field = field_module.findFieldByName("coordinates")
        finite_element_field = coordinate_field.castFiniteElement()
        assert finite_element_field.isValid() and (finite_element_field.getNumberOfComponents() == 3)

        groups = get_group_list(field_module)
        nodes = field_module.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
        node_template = nodes.createNodetemplate()

        params = dict()
        params["group"] = list()
        params["values"] = list()
        cls = 0
        for g in groups:
            group = field_module.findFieldByName(g.getName())
            if group.isValid():
                group = group.castGroup()
                node_group = group.getFieldNodeGroup(nodes)
                if node_group.isValid():
                    group_nodes = node_group.getNodesetGroup()
                    if group_nodes.isValid():
                        node_iter = group_nodes.createNodeiterator()
                        node = node_iter.next()
                        while node.isValid():
                            node_template.defineFieldFromNode(finite_element_field, node)
                            field_cache.setNode(node)
                            node_id = node.getIdentifier()
                            result, values = finite_element_field.getNodeParameters(field_cache, -1,
                                                                                    Node.VALUE_LABEL_VALUE, 1, 3)
                            assert result == RESULT_OK, f"Error extracting parameters for node {node_id}."
                            params["group"].append(cls)
                            params["values"].append((values[0], values[1], values[2]))
                            node = node_iter.next()
            cls += 1

    return params
