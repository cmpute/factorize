use clap::{ArgEnum, Parser};
use num_bigint::BigUint;
use num_prime::nt_funcs::factorize;
use yansi::Color::Green;

#[derive(Debug, Copy, Clone, PartialEq, Eq, ArgEnum)]
enum OutputFormat {
    MATH,
    GNU,
    JSON,
}

/// A command line utility for integer factorization
#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// The integers to factorize
    num: Vec<BigUint>,

    /// Output format of the factorization result
    #[clap(short, long, arg_enum, default_value_t=OutputFormat::MATH)]
    format: OutputFormat,

    /// Print additional information on stderr
    #[clap(short, long)]
    verbose: bool,

    /// Prove each factor to be prime using deterministic Miller-Rabin or Lucas's primality test
    #[clap(short, long)]
    prove: bool

    // TODO: set timeout
    // TODO: display input bits, ETA for big integers in verbose mode
    // TODO: implement [Lucas test](https://en.wikipedia.org/wiki/Lucas_primality_test) and output it in json mode
    // TODO: Profile 103974784173188359291513882659673808303, 114522132269336660310126182173854449539, 52696948083480579404258676877022335423
}

fn main() {
    let args = Args::parse();

    for n in args.num.into_iter() {
        if args.verbose {
            eprintln!("{}", Green.paint(format!("The input {} has {} bits", n, n.bits())));
        }

        // print headers
        match args.format {
            OutputFormat::GNU => print!("{}:", n),
            OutputFormat::MATH => print!("{} =", n),
            OutputFormat::JSON => {}
        };

        // factorize
        let factors = factorize(n);

        // print factors
        match args.format {
            OutputFormat::GNU => {
                for (p, e) in factors.into_iter() {
                    for _ in 0..e {
                        print!(" {}", p);
                    }
                }
                println!();
            },
            OutputFormat::JSON => println!("{{factors: {:?}, complete: true}}", factors),
            OutputFormat::MATH => {
                let mut first = true;
                for (p, e) in factors.into_iter() {
                    if !first {
                        print!(" *");
                    }
                    if e == 1 {
                        print!(" {}", p);
                    } else {
                        print!(" {}^{}", p, e);
                    }
                    first = false;
                }
                println!();
            }
        }
    }
}
