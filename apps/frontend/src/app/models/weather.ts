export interface Weather {
  temperature: number;
  description: string;
  humidity: number;
  wind_speed: number;
  error?: string;
}
