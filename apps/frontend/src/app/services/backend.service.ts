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
        this.http.get<{ 
          destination: string; 
          recommendation: string;
          error?: string;
          raw_response?: string;
        }>(
          `${this.apiUrl}/api/recommend?destination=${encodeURIComponent(destination)}`
        )
      );

      // Check if there was an error from the backend
      if (response.error) {
        console.error('Backend error:', response.error);
        console.error('Raw response:', response.raw_response || response.recommendation);
        alert(`Error: ${response.error}\n\nCheck console for details.`);
        return [];
      }

      // Parse the JSON array from the recommendation string
      const activities = JSON.parse(response.recommendation);
      
      if (!Array.isArray(activities)) {
        console.error('Expected array, got:', typeof activities, activities);
        return [];
      }
      
      return activities;
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      if (error instanceof SyntaxError) {
        console.error('This is a JSON parsing error. The backend returned invalid JSON.');
      }
      return [];
    }
  }
}
