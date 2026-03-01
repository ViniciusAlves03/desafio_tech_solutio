import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ProductService } from '../../../core/services/product';
import { AuthService } from '../../../core/services/auth';
import { Router } from '@angular/router';
import { NotificationService } from '../../../core/services/notification';
import { ConfirmService } from '../../../core/services/confirm';
import { ViewProductService } from '../../../core/services/view-product.service';

@Component({
  selector: 'app-product-list',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './product-list.html',
  styleUrl: './product-list.scss',
})
export class ProductListComponent implements OnInit {
  products: any[] = [];
  currentPage: number = 1;
  totalPages: number = 1;
  totalItems: number = 0;
  perPage: number = 10;
  filterName: string = '';
  filterBrand: string = '';
  private productService = inject(ProductService);
  private authService = inject(AuthService);
  private router = inject(Router);
  private notify = inject(NotificationService);
  private confirmSrv = inject(ConfirmService);
  private viewSrv = inject(ViewProductService);

  ngOnInit(): void {
    this.loadProducts(this.currentPage);
  }

  loadProducts(page: number = 1): void {
    this.currentPage = page;
    this.productService.getProducts(page, 10, this.filterName, this.filterBrand).subscribe({
      next: (response) => {
        this.products = response.items;
        this.totalPages = response.metadata.total_pages;
      },
      error: (err) => console.error('Erro ao carregar produtos', err)
    });
  }

  goToNextPage(): void {
    if (this.currentPage < this.totalPages) {
      this.loadProducts(this.currentPage + 1);
    }
  }

  goToPreviousPage(): void {
    if (this.currentPage > 1) {
      this.loadProducts(this.currentPage - 1);
    }
  }

  onSearch(): void {
    this.loadProducts(1);
  }

  onDelete(id: number): void {
    this.confirmSrv.ask('Tem certeza que deseja eliminar este produto?', () => {
      this.productService.deleteProduct(id).subscribe({
        next: () => {
          this.products = this.products.filter(p => p.id !== id);

          this.notify.show('Pedido de exclusão enviado para a fila.', 'success');
        },
        error: () => this.notify.show('Erro ao excluir produto.', 'error')
      });
    });
  }

  onView(product: any): void {
    this.productService.getProductImage(product.id).subscribe({
      next: (blob) => {
        const imageUrl = URL.createObjectURL(blob);
        this.viewSrv.open({ ...product, imageUrl });
      },
      error: () => {
        this.viewSrv.open(product);
      }
    });
  }

  logout(): void {
    this.authService.logout().subscribe({
      next: () => {
        this.authService.removeToken();
        this.router.navigate(['/login']);
      },
      error: () => {
        this.authService.removeToken();
        this.router.navigate(['/login']);
      }
    });
  }
}
