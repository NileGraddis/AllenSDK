
import requests

from allensdk.core.multi_source_argschema_parser import MultiSourceArgschemaParser

from ._schemas import InputParameters, OutputParameters


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
    ''', sep='')

    response = requests.get(query_url)
    data = response.json()

    return data


def run_unionize(args):

    pass


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

    outputs = run_unionize(mod.args)
    MultiSourceArgschemaParser.write_or_print_outputs(output, mod)


if __name__ == '__main__':
    main()