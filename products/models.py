from django.db import models

class Products(models.Model):
    class CategoryChoices(models.TextChoices):
        SELECT = "Select"
        DOG = "Dog"
        CAT = "Cat"

    Name = models.CharField(max_length=50)
    Category = models.CharField(
        max_length=6, choices=CategoryChoices.choices, default=CategoryChoices.SELECT
    )
    Price = models.DecimalField(max_digits=7, decimal_places=2)
    Description = models.TextField()
    Brand = models.CharField(max_length=20)
    Weight = models.CharField(max_length=20)
    Stock = models.IntegerField()
    Image = models.ImageField(upload_to='products/')
    Ingredient = models.JSONField(default=list)
    is_deleted = models.BooleanField(default=False)
    product_added = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['Category']),  # Index for Category field
            models.Index(fields=['Price']),     # Index for Price field
            models.Index(fields=['Brand']),     # Index for Brand field
            models.Index(fields=['is_deleted']), # Index for is_deleted field
            models.Index(fields=['product_added']), # Index for product_added field
        ]

    def __str__(self):
        return self.Name

    # def delete(self):
    #     self.is_deleted = True
    #     self.save()
