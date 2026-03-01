import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ProductService {
  private apiUrl = `${environment.apiUrl}/products`;
  private http = inject(HttpClient);

  getProducts(page: number = 1, perPage: number = 10, name?: string, brand?: string, sortBy: string = 'id', sortOrder: string = 'asc'): Observable<any> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('per_page', perPage.toString())
      .set('sort_by', sortBy)
      .set('sort_order', sortOrder);

    if (name) params = params.set('name', name);
    if (brand) params = params.set('brand', brand);

    return this.http.get<any>(this.apiUrl, { params });
  }

  getProductById(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${id}`);
  }

  createProduct(productData: FormData): Observable<any> {
    return this.http.post(this.apiUrl, productData);
  }

  updateProduct(id: number, productData: FormData): Observable<any> {
    return this.http.patch(`${this.apiUrl}/${id}`, productData);
  }

  deleteProduct(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }

  getProductImage(id: number): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/${id}/image`, { responseType: 'blob' });
  }
}
