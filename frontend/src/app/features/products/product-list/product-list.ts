import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ProductService } from '../../../core/services/product';
import { AuthService } from '../../../core/services/auth';
import { Router } from '@angular/router';
import { NotificationService } from '../../../core/services/notification';

@Component({
  selector: 'app-product-list',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './product-list.html',
  styleUrl: './product-list.scss',
})
export class ProductListComponent implements OnInit {
  products: any[] = [];
  private productService = inject(ProductService);
  private authService = inject(AuthService);
  private router = inject(Router);
  private notify = inject(NotificationService);

  ngOnInit(): void {
    this.loadProducts();
  }

  loadProducts(): void {
    this.productService.getProducts().subscribe({
      next: (response) => {
        this.products = response.items;
      },
      error: (err) => console.error('Erro ao carregar produtos', err)
    });
  }

  onDelete(id: number): void {
    if (confirm('Tem certeza que deseja eliminar este produto?')) {
      this.productService.deleteProduct(id).subscribe({
        next: () => {
          this.notify.show('Pedido de exclusão enviado para a fila.', 'success');
          this.loadProducts();
        },
        error: () => {
          this.notify.show('Não foi possível excluir o produto.', 'error');
        }
      });
    }
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
