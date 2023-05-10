from mitmproxy.tools.main import mitmdump, run
from mitmproxy.tools import dump
from mitmproxy.tools import cmdline


def main():
    args = ['-p', '8080', '--listen-host', '0.0.0.0', '-s', 'p2.py']

    def extra(args):
        if args.filter_args:
            v = " ".join(args.filter_args)
            return dict(
                save_stream_filter=v,
                readfile_filter=v,
                dumper_filter=v,
            )
        return {}

    run(dump.DumpMaster, cmdline.mitmdump, args, extra)


if __name__ == '__main__':
    main()
