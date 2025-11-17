import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { Activity } from '../models/activity';

@Injectable({
  providedIn: 'root'
})
export class BackendService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  async getRecommendations(destination: string): Promise<Activity[]> {
    try {
      const response = await firstValueFrom(
        this.http.get<{ destination: string; recommendation: string }>(
          `${this.apiUrl}/api/recommend?destination=${encodeURIComponent(destination)}`
        )
      );

      // Parse the JSON array from the recommendation string
      const activities = JSON.parse(response.recommendation);
      return activities;
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      return [];
    }
  }
}
