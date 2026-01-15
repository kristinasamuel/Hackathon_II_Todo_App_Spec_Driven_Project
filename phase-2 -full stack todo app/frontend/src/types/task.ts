export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
  due_date?: string; // ISO date string
  priority: 'low' | 'medium' | 'high';
  category?: string;
  user_id: string;
}