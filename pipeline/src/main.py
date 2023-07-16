from utility.initialise import (
    get_args,
    set_seed,
)


def main(args):

    # Set seed for consistent experiments
    set_seed(args['seed'])
    
    pass


if __name__ == '__main__':
    args = get_args()
    main(args)