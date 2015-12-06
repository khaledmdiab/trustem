"""
TrustEm: Recommendation with disjoint trust network

Usage:
  rec.py mf  [--ip_dir=<ip_dir>] [--uik=<uik>] [--uuk=<uuk>] [--threshold=<threshold>] [--K=<k>] [--steps=<steps>] [--alpha=<alpha>] [--beta=<beta>]

Options:
  -h --help     Show this help message.
  -v --version     Show version.
  --ip_dir=<ip_dir>    Input directory [default: ./]
  --uik=<uik>    user item threshold [default: 10]
  --uuk=<uuk>    user user threshold [default: 100]
  --threshold=<threshold>    Coverage threshold [default: 1]
  --K=<k>    Features count [default: 100]
  --steps=<steps>    GD steps [default: 250]
  --alpha=<alpha>    Reg. parameter [default: 0.0002]
  --beta=<beta>    Reg. parameter [default: 0.02]
"""
import os
import recstats
from docopt import docopt
from gen import DataGen, EP_RATING, EP_TRUST
__author__ = 'Khaled Diab (kdiab@sfu.ca)'

MODELS = ['mf']

if __name__ == '__main__':
    arguments = docopt(__doc__, version='TrustEm 0.1')
    model_name = None
    models_names = [model_str for model_str in MODELS if model_str in arguments and arguments[model_str]]
    if models_names and len(models_names) == 1:
        model_name = models_names[0]

    if not model_name:
        print 'Please insert a valid model name'
        exit(0)
    ip_dir = arguments['--ip_dir']
    rating_file = os.path.join(ip_dir, EP_RATING)
    trust_file = os.path.join(ip_dir, EP_TRUST)
    uik = int(arguments['--uik'])
    uuk = int(arguments['--uuk'])
    generator = DataGen(rating_file, trust_file, uik=uik, uuk=uuk)
    generator.generate()
    print 'User Item Matrix Size:', generator.ui_matrix.shape
    print 'User User Matrix Size:', generator.uu_matrix.shape
    results = None
    threshold = None
    if model_name == 'mf':
        import matrixfac
        K = int(arguments['--K'])
        steps = int(arguments['--steps'])
        alpha = float(arguments['--alpha'])
        beta = float(arguments['--beta'])
        threshold = float(arguments['--threshold'])
        print 'Running MF with K=%d, steps=%d, threshold=%f, alpha=%f and beta=%f' % (K, steps, threshold, alpha, beta)
        results = matrixfac.run_rec(generator, k=K, steps=steps, alpha=alpha, beta=beta)

    print "RMSE: %f" % recstats.rmse(generator.ui_matrix, results)
    print "Coverage: %f " % recstats.coverage(results, threshold if threshold else 1)