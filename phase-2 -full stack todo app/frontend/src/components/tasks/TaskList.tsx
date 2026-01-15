'use client';

import { useState, useEffect } from 'react';
import TaskCard from './TaskCard';
import TaskForm from './TaskForm';
import FeedbackMessage from '../common/FeedbackMessage';
import { Task } from '@/types/task';
import taskService from '@/services/tasks';

const TaskList = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [message, setMessage] = useState<{type: 'success' | 'error'; message: string} | null>(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const fetchedTasks = await taskService.getTasks();
      setTasks(fetchedTasks);
    } catch (error: any) {
      setMessage({
        type: 'error',
        message: error.message || 'Failed to load tasks. Please try again.'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (taskData: Omit<Task, 'id' | 'created_at' | 'updated_at'>) => {
    try {
      const newTask = await taskService.createTask(taskData);
      setTasks([newTask, ...tasks]);
      setShowForm(false);
      setMessage({
        type: 'success',
        message: 'Task created successfully!'
      });
    } catch (error: any) {
      setMessage({
        type: 'error',
        message: error.message || 'Failed to create task. Please try again.'
      });
    }
  };

  const handleUpdateTask = async (id: string, updates: Partial<Task>) => {
    try {
      const updatedTask = await taskService.updateTask(id, updates);
      setTasks(tasks.map(task => task.id === id ? updatedTask : task));
      setMessage({
        type: 'success',
        message: 'Task updated successfully!'
      });
    } catch (error: any) {
      setMessage({
        type: 'error',
        message: error.message || 'Failed to update task. Please try again.'
      });
    }
  };

  const handleDeleteTask = async (id: string) => {
    try {
      await taskService.deleteTask(id);
      setTasks(tasks.filter(task => task.id !== id));
      setMessage({
        type: 'success',
        message: 'Task deleted successfully!'
      });
    } catch (error: any) {
      setMessage({
        type: 'error',
        message: error.message || 'Failed to delete task. Please try again.'
      });
    }
  };

  const handleToggleComplete = async (id: string) => {
    try {
      const task = tasks.find(t => t.id === id);
      if (task) {
        const updatedTask = await taskService.updateTask(id, { completed: !task.completed });
        setTasks(tasks.map(t => t.id === id ? updatedTask : t));
        setMessage({
          type: 'success',
          message: `Task marked as ${!task.completed ? 'completed' : 'incomplete'}!`
        });
      }
    } catch (error: any) {
      setMessage({
        type: 'error',
        message: error.message || 'Failed to update task status. Please try again.'
      });
    }
  };

  const dismissMessage = () => {
    setMessage(null);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        <span className="ml-2 text-gray-600">Loading tasks...</span>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      {message && (
        <FeedbackMessage
          type={message.type}
          message={message.message}
          onClose={dismissMessage}
        />
      )}

      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
        <h2 className="text-2xl font-bold text-gray-900">Your Tasks</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200 font-medium w-full sm:w-auto"
        >
          {showForm ? 'Cancel' : '+ Add Task'}
        </button>
      </div>

      {showForm && (
        <div className="mb-6 bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <TaskForm onSubmit={handleAddTask} onCancel={() => setShowForm(false)} />
        </div>
      )}

      {tasks.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-lg shadow-sm border border-gray-200">
          <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
          <p className="mt-1 text-sm text-gray-500">Get started by creating a new task.</p>
          <div className="mt-6">
            <button
              onClick={() => setShowForm(true)}
              className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Create new task
            </button>
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          {tasks.map(task => (
            <TaskCard
              key={task.id}
              task={task}
              onToggleComplete={handleToggleComplete}
              onUpdate={handleUpdateTask}
              onDelete={handleDeleteTask}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default TaskList;