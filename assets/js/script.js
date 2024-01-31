$(function() {
    $('article img').each(function() {
        var src = $(this).attr('src');
        $(this).wrap('<a href="' + src + '" target="_blank"></a>');
    });
    $('article > h2').each(function() {
        $('nav.toc > ul').append(
            $('<li>')
                .attr('class', 'nav-item')
                .append(
                    $('<a>')
                        .attr('class', 'nav-link')
                        .text($(this).text())
                        .attr('href', '#' + $(this).attr('id'))
                ) 
        );
    });
    $('[data-spy="scroll"]').each(function () {
        var $spy = $(this).scrollspy('refresh')
    });
    $('pre').each(function(index) {
    var generatedId = 'codeBlock' + index;
    var languageClass = $(this).children('code:first').attr('class').split(' ')[0];
    var language = languageClass == 'language-sh' ? 'shell' : 
        languageClass == 'language-js' ? 'javascript' : 
        languageClass == 'language-xml' ? 'xml' : 
        languageClass == 'language-sql' ? 'sql' : 
        languageClass == 'language-csharp' ? 'c#' : 'code';
    $(this).attr('id', generatedId);
    var header = $('<div/>', {
      class: 'code-header mt-3 mb-0 bg-light d-flex justify-content-between border',
    }).append(
        $('<span/>', {     
            class: 'mx-2 text-muted text-capitalize font-weight-light',
        html: language
        })
    ).append(
        $('<button/>', {   
            class: 'm-0 btn btn-code btn-sm btn-light codeBtn rounded-0 border-left text-muted font-weight-light',
        'data-clipboard-target': '#' + generatedId,
        type: 'button'
        }).append(
        $('<i/>', {
            class: 'fa fa-files-o mr-2',
          'aria-hidden': 'true'
        })
      ).append(
        'Copy'
      )
    );
    header.insertBefore($(this));
    $(this).addClass('mt-0');
});
hljs.initHighlightingOnLoad();
new ClipboardJS('.btn-code');
});
