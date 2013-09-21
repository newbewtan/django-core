# -*- coding: utf-8 -*-


class PagingViewMixin(object):

    page_num = 1
    page_size = 15
    paginate_by = page_size
    page_kwarg = 'p'  # used by django's core ListView CBV

    def dispatch(self, *args, **kwargs):

        if self.page_size != self.paginate_by:
            # Default to the paginate_by value if these two if different.
            self.page_size = self.paginate_by

        self.page_num, self.page_size = self.get_paging()
        self.paginate_by = self.page_size
        return super(PagingViewMixin, self).dispatch(*args, **kwargs)

    def get_paging(self):
        """Gets the paging values passed through the query string params.

            * "p" for "page number" and
            * "ps" for "page size".

        :returns: tuple with the page being the first part and the page size
            being the second part.
        """
        orig_page_num = self.page_num
        orig_page_size = self.page_size

        try:

            page_num = int(self.request.GET.get('p'))

            if page_num < 1:
                page_num = orig_page_num
        except:
            page_num = orig_page_num

        try:
            orig_page_size = self.page_size
            page_size = int(self.request.GET.get('ps'))

            if page_size < 1:
                page_size = orig_page_size
        except:
            page_size = orig_page_size

        return page_num, page_size
