import esper

from ..components.regions import Regions, Node, NextNode, Link, Length, Links
from ..components.tags import LinkDue, NodeRegionsDue, LinkRegionsDue
from ..api.labels import entity_by_label
from ..utils import untag_all


class RegionsSystem(esper.Processor):
    def process(self):
        self._assign_links()
        self._assign_node_regions()
        untag_all(LinkDue, NodeRegionsDue, LinkRegionsDue)

    def _assign_node_regions(self):
        for ent, (node, _) in esper.get_components(Node, NodeRegionsDue):
            if node_rg := esper.try_component(entity_by_label(node.label), Regions):
                esper.add_component(ent, Regions(node_rg.regions.copy()))
        
    def _assign_links(self):
        for ent, (node, nxt, _) in esper.get_components(Node, NextNode, LinkDue):
            # Check the current node for links with the next node
            node_ent = entity_by_label(node.label)
            try:
                node_links = esper.component_for_entity(node_ent, Links)
                link_label = node_links.map[nxt.label]
            
            except KeyError:
                esper.dispatch_event("nodes_unlinked_error", ent, node.label, nxt.label)
                continue
                
            link = entity_by_label(link_label)
            
            if link_len := esper.try_component(link, Length):
                l = link_len.length
            else:
                l = 0
            
            # Inherit link regions
            if link_rg := esper.try_component(link, Regions):
                esper.add_component(ent, Regions(link_rg.regions.copy()))
            
            esper.add_component(ent, Link(link_label, l))