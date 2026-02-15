'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useTasks } from '@/hooks/useTasks';
import { useRouter } from 'next/navigation';
import TaskForm from '@/components/tasks/TaskForm';
import TaskList from '@/components/tasks/TaskList';

const TasksPage: React.FC = () => {
  const { user, loading: authLoading, isAuthenticated } = useAuth();
  const { tasks, loading: tasksLoading, error, addTask, updateTask, deleteTask, toggleTaskCompletion } = useTasks();
  const router = useRouter();
  const [editingTaskId, setEditingTaskId] = useState<string | null>(null);
  const [editingTaskTitle, setEditingTaskTitle] = useState('');
  const [editingTaskDescription, setEditingTaskDescription] = useState('');
  const [editingTaskPriority, setEditingTaskPriority] = useState<'low' | 'medium' | 'high'>('medium');
  const [editingTaskDueDate, setEditingTaskDueDate] = useState('');

  // Redirect if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated()) {
      router.push('/login');
    }
  }, [authLoading, isAuthenticated, router]);

  // Show loading state while checking authentication
  if (authLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Checking authentication status...</p>
        </div>
      </div>
    );
  }

  // Redirect if not authenticated
  if (!isAuthenticated()) {
    return null; // Redirect effect will handle this
  }

  const handleAddTask = async (title: string, description: string, priority: 'low' | 'medium' | 'high', dueDate: string) => {
    try {
      await addTask({
        title: title,
        description: description,
        priority: priority,
        dueDate: dueDate
      });
    } catch (err) {
      console.error('Failed to add task:', err);
    }
  };

  const handleToggleTask = async (id: string) => {
    try {
      await toggleTaskCompletion(id);
    } catch (err) {
      console.error('Failed to toggle task:', err);
    }
  };

  const startEditingTask = (task: Task) => {
    setEditingTaskId(task.id);
    setEditingTaskTitle(task.title);
    setEditingTaskDescription(task.description || '');
    setEditingTaskPriority(task.priority || 'medium');
    setEditingTaskDueDate(task.due_date || '');
  };

  const saveEditedTask = async (id: string) => {
    try {
      await updateTask(id, { 
        title: editingTaskTitle, 
        description: editingTaskDescription,
        priority: editingTaskPriority,
        dueDate: editingTaskDueDate
      });
      setEditingTaskId(null);
    } catch (err) {
      console.error('Failed to update task:', err);
    }
  };

  const cancelEditingTask = () => {
    setEditingTaskId(null);
  };

  const handleDeleteTask = async (id: string) => {
    await deleteTask(id);
  };

  const handleUpdateTask = async (id: string, data: any) => {
    try {
      await updateTask(id, data);
    } catch (err) {
      console.error('Failed to update task:', err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="lg:flex lg:items-center lg:justify-between mb-6">
            <div className="min-w-0 flex-1">
              <h1 className="text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:text-3xl sm:tracking-tight">
                My Tasks
              </h1>
              <p className="mt-2 text-gray-600">Manage your tasks efficiently and stay organized</p>
            </div>
          </div>

          <div className="mt-6 grid grid-cols-1 gap-6">
            {/* Task Form */}
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <TaskForm onSubmit={handleAddTask} loading={tasksLoading} error={error} />
            </div>

            {/* Task List */}
            <TaskList
              tasks={tasks}
              loading={tasksLoading}
              error={error}
              onToggleComplete={handleToggleTask}
              onUpdate={handleUpdateTask}
              onDelete={handleDeleteTask}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default TasksPage;