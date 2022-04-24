use clap::Parser;
use num_bigint::BigUint;
use num_prime::nt_funcs::{factorize64, factorize};
use num_traits::ToPrimitive;

/// A command line utility for integer factorization
#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// The integer to factorize
    num: BigUint,

    /// Print additional information on stderr
    #[clap(short, long)]
    verbose: bool

    // TODO: display input bits, ETA for big integers
}

fn main() {
    let args = Args::parse();

    // use shortcuts to prevent formatting big integers when possible
    if let Some(n) = args.num.to_u64() {
        println!("{:?}", factorize64(n));
    } else {
        println!("{:?}", factorize(args.num));
    }
}
