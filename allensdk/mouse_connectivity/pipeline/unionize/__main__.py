import logging
import itertools as it

import requests

from allensdk.core.multi_source_argschema_parser import MultiSourceArgschemaParser

from ._schemas import InputParameters, OutputParameters
from ._unionize import field


def clean_multiline_string(string, sep=' '):
    return sep.join(string.split())


def get_inputs_from_lims(args):
    '''Read inputs for this module from the Allen Institute's internal Laboratory Information Management Database 
    (this is only visible from the Institute's network).

    Paramters
    ---------
    args : argparse.Namespace
        host : str
            The url of the LIMS instance from which input data will be drawn.
        image_series_id : int
            Identifier for the dataset to be unionized
        job_queue_name : str, optional
            Identifies the type of unionizes to be computed. Defaults to TISSUECYTE_UNIONIZE_CLASSIC_QUEUE. Check the 
            job_queues table in LIMS for current information on available queues.
        
    Notes
    -----
    This module writes its outputs directly into the output json file. Use --output_json <path_to_file.json> 
    on the command line to specify a local output path.

    '''
    
    host = args.host
    image_series_id = args.image_series_id
    job_queue_name = args.job_queue_name

    query_url = clean_multiline_string('''
        {}/input_jsons?
        strategy_class=TissuecyteUnionizeBaseStrategy&
        object_class=ImageSeries&
        object_id={}&
        job_queue_name={}
    '''.format(host, image_series_id, job_queue_name), sep='')

    response = requests.get(query_url)
    data = response.json()
    return data


# TODO: move this - or just use registered class names
FIELD_MAP = {
    'sum_pixels': field.SumPixelsField,
    'sum_projecting_pixels': field.SumProjectingPixelsField,
    'projection_density': field.ProjectionDensityField
}


def run_unionize(args):

    args['requested_fields'] = ['sum_pixels', 'sum_projecting_pixels', 'projection_density'] # TODO this is a placeholder

    # setup fields
    fields = {}
    interval_requirements = {} # TODO: gotta flip these
    field_requirements = {}

    key_iter = it.product(args['structures'], args['hemisphere_ids'], (True, False), args['requested_fields'])
    for structure, hemisphere_id, injection_status, requested_field in key_iter:
        key = field.Key(structure['id'], hemisphere_id, injection_status, requested_field)
        fields[key] = FIELD_MAP[requested_field](key)

        field_requirements[key] = fields[key].required_fields
        interval_requirements[key] = fields[key].required_intervals

    print(interval_requirements)
    print(field_requirements)

    # setup field dependency queues

    # set constant fields

    # load interval data

    # fill interval fields

    # drop interval data

    # field loop

    # propagate fields

    # organize unionizes

    return {}


def main():

    mod = MultiSourceArgschemaParser(
        {
            'lims': {
                'get_input_data': get_inputs_from_lims,
                'params': {
                    'host': 'http://lims2',
                    'image_series_id': None,
                    'job_queue_name': 'TISSUECYTE_UNIONIZE_CLASSIC_QUEUE'
                }
            }
        },
        schema_type=InputParameters,
        output_schema_type=OutputParameters
    )

    output = run_unionize(mod.args)
    MultiSourceArgschemaParser.write_or_print_outputs(output, mod)


if __name__ == '__main__':
    main()