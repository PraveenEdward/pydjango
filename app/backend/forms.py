from django import forms
from .models import (
    Category,
    Product,
    Invoice,
    InvoiceItem,
    Settings
)

class ProductExcelUploadForm(forms.Form):

    excel_file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = '__all__'

        widgets = {
            'shop_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'invoice_prefix': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'currency_symbol': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'logo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
        }),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

        widgets = {
            'category_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Category Name'
            })
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),

            'barcode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Scan or Enter Barcode'
            }),

            'product_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'purchase_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),

            'selling_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),

            'stock': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'minimum_stock': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice

        exclude = (
            'invoice_no',
            'total_qty',
            'total_amount',
            'grand_total',
        )

        widgets = {

            'customer_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Customer Name'
                }
            ),

            'customer_mobile': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Mobile Number'
                }
            ),

            'payment_method': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'discount_amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01',
                    'placeholder': '0.00'
                }
            ),
        }

    def clean_discount_amount(self):

        discount = self.cleaned_data.get(
            'discount_amount'
        )

        if discount is None:
            return 0

        return discount


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem

        fields = (
            'product',
            'quantity',
        )

        widgets = {

            'product': forms.Select(attrs={
                'class': 'form-control select2'
            }),

            'quantity': forms.NumberInput(attrs={
                'class': 'form-control qty',
                'min': '1',
                'value': '1'
            }),
        }

class BarcodeScanForm(forms.Form):

    barcode = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'barcode',
                'placeholder': 'Scan Barcode',
                'autofocus': True
            }
        )
    )

