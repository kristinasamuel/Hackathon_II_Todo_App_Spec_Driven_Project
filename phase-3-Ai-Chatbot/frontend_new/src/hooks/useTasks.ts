'use client';

import { useState, useEffect } from 'react';
import { Task, NewTask, UpdateTask, taskService } from '@/services/tasks';

export const useTasks = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const tasksData = await taskService.getTasks();
      setTasks(tasksData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  const addTask = async (taskData: NewTask) => {
    try {
      setError(null);
      const newTask = await taskService.createTask(taskData);
      setTasks(prev => [...prev, newTask]);
      return { success: true, task: newTask };
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to add task';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const updateTask = async (taskId: string, taskData: UpdateTask) => {
    try {
      setError(null);
      const updatedTask = await taskService.updateTask(taskId, taskData);

      setTasks(prev =>
        prev.map(task =>
          task.id === taskId ? updatedTask : task
        )
      );

      return { success: true, task: updatedTask };
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update task';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const deleteTask = async (taskId: string) => {
    try {
      setError(null);
      await taskService.deleteTask(taskId);

      setTasks(prev =>
        prev.filter(task => task.id !== taskId)
      );

      return { success: true };
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete task';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const toggleTaskCompletion = async (taskId: string) => {
    try {
      setError(null);
      const updatedTask = await taskService.toggleTaskCompletion(taskId);

      setTasks(prev =>
        prev.map(task =>
          task.id === taskId ? updatedTask : task
        )
      );

      return { success: true, task: updatedTask };
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to toggle task completion';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  return {
    tasks,
    loading,
    error,
    addTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
    refetch: fetchTasks,
  };
};