
from argschema.schemas import ArgSchema, DefaultSchema
from argschema.fields import Nested, Dict, String, Int, Float, List


class Structure(DefaultSchema):
    id = Int(required=True, help='unique identifier for this structure')
    parent_structure_id = Int(required=True, allow_none=True, help='Identifier of this structure\'s ontological parent (containing structure)')
    name = String(required=False, help='long form human readable identifier for this structure')
    acronym = String(required=False, help='short form human readable identifier for this structure')

class InputParameters(ArgSchema):
    grid_paths = Dict(required=True, keys=String, values=String, help='maps volume types (understood by the module) to filesystem paths')
    structures = Nested(Structure, required=True, many=True, help='Defines the brain structures over which to compute unionizes')
    hemisphere_ids = List(Int, required=True, help='Defines the hemispheres over which to compute unionizes (1: left, 2: right, 3: both)')
    image_series_id = Int(required=True, help='Identifier for the image series to be unionized. This gets written to each output unionize')
    annotation_path = String(required=True, help='Filesystem path to annotation volume (label array mapping voxels to structures).')
    slice_thickness = Float(required=True, help='Distance in microns betweens successive scanned slices')
    reference_spacing = Float(required=True, help='Isometric resolution in microns of the reference space')
    reference_shape = List(Int, required=True, help='3-long array whose values are the length of each axis of the reference volume')
    image_resolution = Float(required=True, help='The side-length (microns) of each pixel in the acquired image.')


class OutputParameters(DefaultSchema):
    unionizes = List(Dict, required=True, help='the output unionize records')