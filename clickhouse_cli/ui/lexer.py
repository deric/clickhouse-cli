import re

from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import Punctuation, Text, Comment, Operator, Keyword, Name, String, Number, Generic, Whitespace

from clickhouse_cli.clickhouse.definitions import (
    CASE_INSENSITIVE_FUNCTIONS,
    DATATYPES,
    FORMATS,
    FUNCTIONS,
    AGGREGATION_FUNCTIONS,
    KEYWORDS,
    OPERATORS,
)
from sqlparse import tokens

line_re = re.compile('.*?\n')

CH_REGEX = [
    (r'\s+', tokens.Text),
    (r'(--\s*).*?\n', tokens.Comment),
    (r'/\*', tokens.Comment.Multiline),
    (r'[0-9]+', tokens.Number),
    (r'[0-9]*\.[0-9]+(e[+-][0-9]+)', tokens.Number),
    (r"'(\\\\|\\'|''|[^'])*'", tokens.String),
    (r'"(\\\\|\\"|""|[^"])*"', tokens.String),
    (r"`(\\\\|\\`|``|[^`])*`", tokens.String),
    (r'[+*/<>=~!@#%^&|`?-]', tokens.Operator),

    (words(OPERATORS, prefix=r'(?i)', suffix=r'\b'), tokens.Keyword),
    (words(DATATYPES, suffix=r'\b'), tokens.Keyword.Type),

    (words(FORMATS), tokens.Name.Label),
    (words(AGGREGATION_FUNCTIONS, suffix=r'(\s*)(\()'),
        bygroups(tokens.Name.Function, tokens.Text, tokens.Punctuation)),
    (words(CASE_INSENSITIVE_FUNCTIONS, prefix=r'(?i)', suffix=r'\b'),
        tokens.Name.Function),
    (words(FUNCTIONS, suffix=r'(\s*)(\()'),
        bygroups(tokens.Name.Function, tokens.Text, tokens.Punctuation)),
    (words(KEYWORDS, prefix=r'(?i)', suffix=r'\b'), tokens.Keyword),
    (r'^\\(\?|\w+)', tokens.Text),

    (r'(?i)[a-z_]\w*', tokens.Text),
    (r'(?i)[;:()\[\],.]', tokens.Punctuation),

    (r"'", tokens.String.Single),
    (r'[a-z_]\w*', tokens.Name),

    (r'[;:()\[\]{},.]', tokens.Punctuation),
]


class CHLexer(RegexLexer):
    name = 'Clickhouse'
    aliases = ['clickhouse']
    filenames = ['*.sql']
    mimetypes = ['text/x-clickhouse-sql']

    tokens = {
        'root': [
            (r'\s+', Text),
            (r'(--\s*).*?\n', Comment),
            (r'/\*', Comment.Multiline, 'multiline-comments'),
            (r'[0-9]+', Number),
            (r'[0-9]*\.[0-9]+(e[+-][0-9]+)', Number),
            (r"'(\\\\|\\'|''|[^'])*'", String),
            (r'"(\\\\|\\"|""|[^"])*"', String),
            (r"`(\\\\|\\`|``|[^`])*`", String),
            (r'[+*/<>=~!@#%^&|`?-]', Operator),

            (words(OPERATORS, prefix=r'(?i)', suffix=r'\b'), Keyword),
            (words(DATATYPES, suffix=r'\b'), Keyword.Type),

            (words(FORMATS), Name.Label),
            (words(AGGREGATION_FUNCTIONS, suffix=r'(\s*)(\()'),
                bygroups(Name.Function, Text, Punctuation)),
            (words(CASE_INSENSITIVE_FUNCTIONS, prefix=r'(?i)', suffix=r'\b'),
                Name.Function),
            (words(FUNCTIONS, suffix=r'(\s*)(\()'),
                bygroups(Name.Function, Text, Punctuation)),
            (words(KEYWORDS, prefix=r'(?i)', suffix=r'\b'), Keyword),
            (r'^\\(\?|\w+)', Text),

            (r'(?i)[a-z_]\w*', Text),
            (r'(?i)[;:()\[\],.]', Punctuation),

            (r"'", String.Single, 'string'),
            (r'[a-z_]\w*', Name),

            (r'[;:()\[\]{},.]', Punctuation),
        ],
        'multiline-comments': [
            (r'/\*', Comment.Multiline, 'multiline-comments'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[^/*]+', Comment.Multiline),
            (r'[/*]', Comment.Multiline)
        ],
        'string': [
            (r"[^']+", String.Single),
            (r"''", String.Single),
            (r"'", String.Single, '#pop'),
        ],
        'quoted-ident': [
            (r'[^"]+', String.Name),
            (r'""', String.Name),
            (r'"', String.Name, '#pop'),
        ],
    }


class CHPrettyFormatLexer(RegexLexer):
    tokens = {
        'root': [
            (r'([^┌─┬┐│││└─┴┘├─┼┤]+)', Generic.Output),
            (r'([┌─┬┐│││└─┴┘├─┼┤]+)', Whitespace),
        ]
    }
