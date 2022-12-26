#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

import argparse

import damo_stat

import _damo_fmt_str
import _damo_subcmds
import _damon

def pr_schemes_tried_regions(kdamonds):
    print('# <kdamond> <context> <scheme>')
    print('# <regions>')
    print('# ...')
    for kdamond in kdamonds:
        for ctx in kdamond.contexts:
            for scheme in ctx.schemes:
                print('%s %s %s' % (kdamond.name, ctx.name, scheme.name))
                print('\n'.join('%s' % r for r in scheme.tried_regions))

def update_pr_schemes_tried_regions():
    if _damon.any_kdamond_running():
        for name in _damon.current_kdamond_names():
            err = _damon.update_schemes_stats(name)
            if err != None:
                print('update schemes stat fail:', err)
                exit(1)
            if _damon.feature_supported('schemes_tried_regions'):
                err = _damon.update_schemes_tried_regions(name)
                if err != None:
                    print('update schemes tried regions fail: %s', err)
                    exit(1)
    content = _damon.read_damon_fs()
    kdamonds = _damon.current_kdamonds()
    pr_schemes_tried_regions(kdamonds)

def update_pr_schemes_stats(raw_nr):
    if _damon.any_kdamond_running():
        for name in _damon.current_kdamond_names():
            err = _damon.update_schemes_stats(name)
            if err != None:
                print('update schemes stat fail:', err)
                exit(1)
    content = _damon.read_damon_fs()
    kdamonds = _damon.current_kdamonds()
    
    print('# <kdamond> <context> <scheme> <field> <value>')
    for kdamond in kdamonds:
        for ctx in kdamond.contexts:
            for scheme in ctx.schemes:
                print('%s %s %s %s %s' % (kdamond.name, ctx.name, scheme.name,
                    'nr_tried', _damo_fmt_str.format_nr(
                        scheme.stats.nr_tried, raw_nr)))
                print('%s %s %s %s %s' % (kdamond.name, ctx.name, scheme.name,
                    'sz_tried', _damo_fmt_str.format_sz(
                        scheme.stats.sz_tried, raw_nr)))
                print('%s %s %s %s %s' % (kdamond.name, ctx.name, scheme.name,
                    'nr_applied', _damo_fmt_str.format_nr(
                        scheme.stats.nr_applied, raw_nr)))
                print('%s %s %s %s %s' % (kdamond.name, ctx.name, scheme.name,
                    'sz_applied', _damo_fmt_str.format_sz(
                        scheme.stats.sz_applied, raw_nr)))
                print('%s %s %s %s %s' % (kdamond.name, ctx.name, scheme.name,
                    'qt_exceeds', _damo_fmt_str.format_nr(
                        scheme.stats.qt_exceeds, raw_nr)))

def set_argparser(parser):
    damo_stat.set_common_argparser(parser)
    parser.add_argument('--raw', action='store_true',
            help='print number in mchine friendly raw form')

def __main(args):
    if args.stat_type == 'schemes_stats':
        update_pr_schemes_stats(args.raw)
    elif args.stat_type == 'schemes_tried_regions':
        update_pr_schemes_tried_regions()

def main(args=None):
    if not args:
        parser = argparse.ArgumentParser()
        set_argparser(parser)
        args = parser.parse_args()

    # Require root permission
    _damon.ensure_root_permission()
    _damon.ensure_initialized(args)

    damo_stat.run_count_delay(__main, args)

    for i in range(args.count):
        if i != args.count - 1:
            time.sleep(args.delay)

if __name__ == '__main__':
    main()