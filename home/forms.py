
'''from django import forms
from home.models import Order  # Make sure to import your model

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order  # Use your order model
        fields = ['title', 'priority', 'description', 'file']  # Include the file field

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['priority'].widget.attrs.update({'class': 'form-select'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['file'].widget.attrs.update({'class': 'form-control'})  # Add file field styling
         
          
           
        form = OrderForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():  
            order = Order(
                client_name=form.cleaned_data['client_name'],
                quantity=form.cleaned_data['quantity'],
                priority=form.cleaned_data['priority'],
                description=form.cleaned_data['description'],
                title=form.cleaned_data['title']
            )
            order.save() 
            messages.success(request, "Your order has been placed successfully.")

            return redirect('success')  
        else:
            messages.error(request, "There was an error with your order form.")
    else:
        form = OrderForm()  

    return render(request, 'orders.html', {
        'form': form,
        'random_images': random_images  # Pass images to the template
    })
 '''