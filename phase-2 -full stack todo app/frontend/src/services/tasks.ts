import api from './api';
import { Task } from '@/types/task';
import logger from '../utils/logger';

class TaskService {
  /**
   * Get all tasks for the authenticated user
   */
  async getTasks(): Promise<Task[]> {
    try {
      logger.info('Fetching all tasks for authenticated user');
      const response = await api.get('/api/tasks');
      logger.info('Tasks fetched successfully', { count: response.data.tasks?.length || response.data.length });
      return response.data.tasks || response.data;
    } catch (error: any) {
      logger.error('Error fetching tasks', { error: error.response?.data?.message || error.message }, error);
      throw new Error(error.response?.data?.message || 'Failed to fetch tasks');
    }
  }

  /**
   * Create a new task
   */
  async createTask(taskData: Omit<Task, 'id' | 'created_at' | 'updated_at' | 'user_id'>): Promise<Task> {
    try {
      logger.info('Creating new task', { title: taskData.title });
      const response = await api.post('/api/tasks', taskData);
      logger.info('Task created successfully', { taskId: response.data.id, title: response.data.title });
      return response.data;
    } catch (error: any) {
      logger.error('Error creating task', {
        title: taskData.title,
        error: error.response?.data?.message || error.message
      }, error);
      throw new Error(error.response?.data?.message || 'Failed to create task');
    }
  }

  /**
   * Update an existing task
   */
  async updateTask(id: string, updates: Partial<Task>): Promise<Task> {
    try {
      logger.info('Updating task', { taskId: id, updates: Object.keys(updates) });
      const response = await api.put(`/api/tasks/${id}`, updates);
      logger.info('Task updated successfully', { taskId: response.data.id, title: response.data.title });
      return response.data;
    } catch (error: any) {
      logger.error('Error updating task', {
        taskId: id,
        updates,
        error: error.response?.data?.message || error.message
      }, error);
      throw new Error(error.response?.data?.message || 'Failed to update task');
    }
  }

  /**
   * Delete a task
   */
  async deleteTask(id: string): Promise<void> {
    try {
      logger.info('Deleting task', { taskId: id });
      await api.delete(`/api/tasks/${id}`);
      logger.info('Task deleted successfully', { taskId: id });
    } catch (error: any) {
      logger.error('Error deleting task', {
        taskId: id,
        error: error.response?.data?.message || error.message
      }, error);
      throw new Error(error.response?.data?.message || 'Failed to delete task');
    }
  }

  /**
   * Toggle task completion status
   */
  async toggleTaskCompletion(id: string): Promise<Task> {
    try {
      logger.info('Toggling task completion', { taskId: id });
      const response = await api.patch(`/api/tasks/${id}/complete`, { completed: true });
      logger.info('Task completion toggled successfully', {
        taskId: response.data.id,
        completed: response.data.completed
      });
      return response.data;
    } catch (error: any) {
      logger.error('Error toggling task completion', {
        taskId: id,
        error: error.response?.data?.message || error.message
      }, error);
      throw new Error(error.response?.data?.message || 'Failed to toggle task completion');
    }
  }

  /**
   * Get a specific task by ID
   */
  async getTaskById(id: string): Promise<Task> {
    try {
      logger.info('Fetching specific task', { taskId: id });
      const response = await api.get(`/api/tasks/${id}`);
      logger.info('Task fetched successfully', { taskId: response.data.id, title: response.data.title });
      return response.data;
    } catch (error: any) {
      logger.error('Error fetching task by ID', {
        taskId: id,
        error: error.response?.data?.message || error.message
      }, error);
      throw new Error(error.response?.data?.message || 'Failed to fetch task');
    }
  }
}

export default new TaskService();