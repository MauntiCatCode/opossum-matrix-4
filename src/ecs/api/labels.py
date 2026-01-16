import esper

from components.labels import Label, LabelEntityMap

def label_exists(label: Label, singleton: int = 1):
    label_map = esper.component_for_entity(singleton, LabelEntityMap).map
    return label in label_map.keys()