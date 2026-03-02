import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { ProductService } from '../../../core/services/product';
import { NotificationService } from '../../../core/services/notification';

@Component({
  selector: 'app-product-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './product-form.html',
  styleUrl: './product-form.scss',
})
export class ProductFormComponent implements OnInit {
  productForm: FormGroup;
  isEditMode = false;
  productId: number | null = null;
  selectedFile: File | null = null;
  isLoading = false;

  private fb = inject(FormBuilder);
  private productService = inject(ProductService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private notify = inject(NotificationService);

  constructor() {
    this.productForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(2)]],
      brand: ['', [Validators.required, Validators.minLength(2)]],
      price: ['', [Validators.required, Validators.min(0.01)]],
      quantity: [0, [Validators.required, Validators.min(0)]]
    });
  }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.isEditMode = true;
      this.productId = +id;
      this.loadProductData(this.productId);
    }
  }

  loadProductData(id: number): void {
    this.productService.getProductById(id).subscribe({
      next: (product) => {
        if (product) {
          this.productForm.patchValue({
            name: product.name,
            brand: product.brand,
            price: product.price,
            quantity: product.quantity
          });
        }
      },
      error: () => {
        this.notify.show('Erro ao carregar dados do produto.', 'error');
        this.router.navigate(['/products']);
      }
    });
  }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
    }
  }

  onSubmit(): void {
    if (this.productForm.invalid) {
      this.productForm.markAllAsTouched();
      return;
    }

    this.isLoading = true;
    const formData = new FormData();
    formData.append('name', this.productForm.get('name')?.value);
    formData.append('brand', this.productForm.get('brand')?.value);
    formData.append('price', this.productForm.get('price')?.value);
    formData.append('quantity', this.productForm.get('quantity')?.value);

    if (this.selectedFile) {
      formData.append('image', this.selectedFile);
    }

    const request = this.isEditMode && this.productId
      ? this.productService.updateProduct(this.productId, formData)
      : this.productService.createProduct(formData);

    request.subscribe({
      next: (response: any) => {
        const msg = response?.message || 'Operação realizada com sucesso.';
        this.notify.translateAndShow(msg, 'success');
        setTimeout(() => this.router.navigate(['/products']), 1500);
      },
      error: (err) => {
        this.isLoading = false;
        const rawMsg = err.error?.description || err.error?.message || 'Erro ao processar produto.';
        this.notify.translateAndShow(rawMsg, 'error');
      }
    });
  }
}
