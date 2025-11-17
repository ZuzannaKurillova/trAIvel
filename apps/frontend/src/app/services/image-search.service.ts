import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ImageSearchService {
  constructor() {}

  async getImage(query: string): Promise<string> {
    // TODO: Implement image search later
    // For now, return a placeholder
    return 'https://via.placeholder.com/400x300?text=' + encodeURIComponent(query);
  }
}
