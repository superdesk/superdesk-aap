def format_text_content(tag, end_with_crlf=True, crlf_count=2):
    """Get text content of an tag

    :param bool end_with_crlf: Appends 2 crlf to end of text
    :param int crlf_count: number of crlf to append
    """
    para_text = ''.join(tag.itertext(with_tail=True)).strip().replace('\n', ' ').replace('\xa0', ' ')
    if para_text != '' and end_with_crlf:
        crlf = []
        for i in range(crlf_count):
            crlf.append('\r\n')
        return '{}{}'.format(para_text, ''.join(crlf))
    elif para_text != '':
        return para_text
    else:
        return ''
