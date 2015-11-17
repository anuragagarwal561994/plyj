#!/usr/bin/env python2

import parser
import model


class BaseFilter(model.Visitor):
    def __init__(self, filter_dict):
        super(BaseFilter, self).__init__()

        if not isinstance(filter_dict, dict):
            raise Exception("Expected dictionary argument")

        self._filter_dict = filter_dict
        self.instances = []

    def clean_instances(self):
        self.instances = []


class MethodInvocationFilter(BaseFilter):
    def __init__(self, filter_dict):
        super(MethodInvocationFilter, self).__init__(filter_dict)

    def visit_MethodInvocation(self, method_invocation):
        method_invocation_dict = method_invocation.__dict__
        if all(value(method_invocation_dict[key]) for key, value in self._filter_dict.iteritems()):
            self.instances.append(method_invocation)

        return True


if __name__ == '__main__':
    # for testing
    p = parser.Parser()

    expressions = [
        'addJavascriptInterface()',
        'not_addJavascriptInterface()',
        'web.addJavascriptInterface()',
    ]

    filter = MethodInvocationFilter(
        {'name': lambda x: x == 'addJavascriptInterface'}
    )

    for expr in expressions:
        tree = p.parse_expression(expr)
        tree.accept(filter)

        print('parsing expression {}'.format(expr))
        print filter.instances, '\n'

        filter.clean_instances()

    statements = [
        'public class Something { public void function1(){ addJavascriptInterface(1, 2); } }'
    ]

    for statement in statements:
        tree = p.parse_statement(statement)
        tree.accept(filter)

        print('parsing statement {}'.format(statement))
        print filter.instances, '\n'

        filter.clean_instances()
