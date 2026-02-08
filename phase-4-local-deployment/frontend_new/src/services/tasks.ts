import api from './api';

export interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
  user_id: string;
}

export interface NewTask {
  title: string;
  description: string;
}

export interface UpdateTask {
  title?: string;
  description?: string;
  completed?: boolean;
}

class TaskService {
  async getTasks(): Promise<Task[]> {
    try {
      const response = await api.get(`/api/tasks`);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch tasks');
    }
  }

  async createTask(task: NewTask): Promise<Task> {
    try {
      const response = await api.post(`/api/tasks`, task);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to create task');
    }
  }

  async updateTask(taskId: string, task: UpdateTask): Promise<Task> {
    try {
      const response = await api.put(`/api/tasks/${taskId}`, task);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to update task');
    }
  }

  async deleteTask(taskId: string): Promise<void> {
    try {
      await api.delete(`/api/tasks/${taskId}`);
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to delete task');
    }
  }

  async toggleTaskCompletion(taskId: string): Promise<Task> {
    try {
      const response = await api.patch(`/api/tasks/${taskId}/complete`);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to toggle task completion');
    }
  }
}

export const taskService = new TaskService();
export default taskService;