import { Routes } from '@angular/router';
import { LoginComponent } from './features/auth/login/login';
import { ProductListComponent } from './features/products/product-list/product-list';
import { ProductFormComponent } from './features/products/product-form/product-form';
import { authGuard } from './core/guards/auth-guard';
import { RegisterComponent } from './features/auth/register/register';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  {
    path: 'products',
    canActivate: [authGuard],
    children: [
      { path: '', component: ProductListComponent },
      { path: 'new', component: ProductFormComponent },
      { path: 'edit/:id', component: ProductFormComponent }
    ]
  },
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: '**', redirectTo: '/login' }
];
