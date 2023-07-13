import datetime
import io
import operator
import os

from foodgram_backend.settings import base
from fpdf import FPDF


class FoodgramPDF(FPDF):
    """Переопределение класса настройки пдф-страницы списка покупок."""

    def __init__(self, side_margin: float, top_margin: float,
                 number_col_need: bool, checkbox_col_need: bool, h_gap: float,
                 v_gap: float, *args, **kwargs,) -> None:
        super().__init__(*args, **kwargs)

        self.side_margin = side_margin
        self.top_margin = top_margin
        self.margins = (self.side_margin, self.top_margin, self.side_margin)
        self.number_col_need = number_col_need
        self.checkbox_col_need = checkbox_col_need
        self.h_gap = h_gap
        self.v_gap = v_gap

        self.add_font('Montserrat', '',
                      os.path.join(base.BASE_DIR,
                                   'media',
                                   'fonts',
                                   'Montserrat-Regular.ttf'))
        self.add_font('Montserrat', 'I',
                      os.path.join(base.BASE_DIR,
                                   'media',
                                   'fonts',
                                   'Montserrat-Italic.ttf'))
        self.add_font('Montserrat', 'B',
                      os.path.join(base.BASE_DIR,
                                   'media',
                                   'fonts',
                                   'Montserrat-Bold.ttf'))
        self.add_font('Montserrat', 'BI',
                      os.path.join(base.BASE_DIR,
                                   'media',
                                   'fonts',
                                   'Montserrat-BoldItalic.ttf'))

        self.set_margins(*self.margins)

    def header(self):
        """Верхний колонтитул страницы."""
        title = (
            f'Список покупок от {datetime.date.today().strftime("%x")}'
        ).upper()
        self.set_font('montserrat', 'B', 14)
        title_width = self.get_string_width(title) + 6
        self.set_x((self.w - title_width) / 2)
        self.set_line_width(1)
        self.cell(
            w=title_width,
            h=15,
            txt=title,
            border=False,
            align='C',
        )
        self.ln(self.t_margin * 2 + self.font_size)

    def footer(self):
        """Нижний колонтитул страницы."""
        self.set_margin(0)
        self.set_y(-20)
        self.set_font('montserrat', '', 12)
        self.set_text_color(255)
        self.set_fill_color(0)
        img_cell_width = 25
        img_width = 12
        page_no_str = f'стр. {self.page_no()}'
        page_no_width = self.get_string_width(page_no_str) + 10
        footer_height = 20
        label = 'Продуктовый помощник'
        self.cell(img_cell_width, footer_height,
                  fill=True)
        self.cell(self.w - img_cell_width - page_no_width,
                  footer_height, label.capitalize(), fill=True)
        self.cell(page_no_width - 8, footer_height, page_no_str,
                  fill=True, align='R')
        self.cell(8, footer_height, fill=True)
        self.image(os.path.join(base.BASE_DIR,
                                'media',
                                'logo',
                                'favicon.png'),
                   w=img_width,
                   keep_aspect_ratio=True,
                   x=img_cell_width - img_width - 5,
                   y=self.h - img_width - (footer_height - img_width) / 2)
        self.set_margins(*self.margins)

    def set_cell_height(self, v_gap: float):
        """Установка высоты ячейки в зависимости от размера шрифта."""
        self.cell_height = self.font_size + v_gap * 2

    def get_column_params(self, itemset,
                          h_gap: float, text_align, cell_border):
        """Определение параметров столбцов и атрибутов ячеек."""

        itemset_col_count = min(len(item) for item in itemset)
        longest_value = []
        for i in range(itemset_col_count):
            func = operator.itemgetter(i)
            longest_value.append(
                max(map(func, itemset), key=self.get_string_width))
        longest_value_index = longest_value.index(max(longest_value, key=len))

        column_idx_offset = 1
        column_params = {}

        if self.number_col_need:
            number_col_width = self.get_string_width(
                f'{len(itemset)}.') + h_gap
            column_idx = column_idx_offset
            column_params.update(
                {column_idx: {
                    'col_width': number_col_width,
                    'col_align': 'CENTER',
                    'cell_border': cell_border,
                    'checkbox_size': None,
                    'txt_index': 'number',
                    'ln': False}
                 }
            )

        if self.checkbox_col_need:
            table_columns_count = itemset_col_count + (
                int(self.checkbox_col_need) + int(self.number_col_need))
            column_params.update(
                {table_columns_count: {
                    'col_width': self.cell_height,
                    'col_align': 'CENTER',
                    'cell_border': cell_border,
                    'checkbox_size': self.font_size,
                    'txt_index': 'checkbox',
                    'ln': False}
                 }
            )

        for col in range(itemset_col_count):
            if col != longest_value_index:
                column_idx = col + column_idx_offset + \
                    int(self.number_col_need)
                col_width = self.get_string_width(longest_value[col]) + h_gap
                col_align = text_align[col]
                column_params.update(
                    {column_idx: {
                        'col_width': col_width,
                        'col_align': col_align,
                        'cell_border': cell_border,
                        'checkbox_size': None,
                        'txt_index': col,
                        'ln': False}
                     }
                )

        temp_gen = (i for i in column_params.items())
        func1 = operator.itemgetter(1)
        func2 = operator.itemgetter('col_width')
        columns_widths_list = list((func2(func1(item))) for item in temp_gen)
        columns_width = sum(columns_widths_list)
        col_longest_width = self.epw - columns_width
        col_longest_align = text_align[longest_value_index]
        column_longest_idx = longest_value_index + column_idx_offset + \
            int(self.number_col_need)
        column_params.update(
            {column_longest_idx: {
                'col_width': col_longest_width,
                'col_align': col_longest_align,
                'cell_border': cell_border,
                'checkbox_size': None,
                'txt_index': longest_value_index,
                'ln': False}
             }
        )
        column_params = sorted(column_params.items())
        column_params[-1][1]['ln'] = True
        return column_params


def create_shopping_file(itemset):
    """Создание файла со списком покупок."""
    pdf = FoodgramPDF(orientation='portrait',
                      unit='mm',
                      format='A4',
                      side_margin=9,
                      top_margin=5,
                      number_col_need=True,
                      checkbox_col_need=True,
                      h_gap=3,
                      v_gap=2)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=23)
    pdf.set_font('Montserrat', '', size=12)
    pdf.set_cell_height(v_gap=pdf.v_gap)
    txt_align = ('LEFT', 'RIGHT', 'LEFT')
    colparams = pdf.get_column_params(itemset=itemset,
                                      h_gap=pdf.h_gap,
                                      text_align=txt_align,
                                      cell_border=False)
    for num, item in enumerate(itemset):
        for col in colparams:
            height = pdf.cell_height
            if col[1].get('txt_index') == 'number':
                txt = f'{num + 1}.'
            elif col[1].get('txt_index') == 'checkbox':
                txt = ' '
                pdf.rect(
                    x=pdf.epw + pdf.l_margin - col[1].get('checkbox_size') - (
                        col[1].get('col_width') - col[1].get('checkbox_size')
                    ) / 2,
                    y=pdf.y + pdf.v_gap,
                    w=col[1].get('checkbox_size'),
                    h=col[1].get('checkbox_size')
                )
            else:
                txt = item[col[1].get('txt_index')]
            pdf.cell(
                w=col[1].get('col_width'),
                h=height,
                txt=txt,
                border=col[1].get('cell_border'),
                align=col[1].get('col_align'),
                ln=col[1].get('ln')
            )
    file = io.BytesIO()
    pdf.output(file)
    file.seek(0)
    return file
