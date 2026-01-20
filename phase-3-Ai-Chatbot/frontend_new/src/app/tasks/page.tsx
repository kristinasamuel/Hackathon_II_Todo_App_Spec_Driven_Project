'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useTasks } from '@/hooks/useTasks';
import { useRouter } from 'next/navigation';

const TasksPage: React.FC = () => {
  const { user, loading: authLoading, isAuthenticated } = useAuth();
  const { tasks, loading: tasksLoading, error, addTask, updateTask, deleteTask, toggleTaskCompletion } = useTasks();
  const router = useRouter();
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');
  const [editingTaskId, setEditingTaskId] = useState<string | null>(null);
  const [editingTaskTitle, setEditingTaskTitle] = useState('');
  const [editingTaskDescription, setEditingTaskDescription] = useState('');

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

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!newTaskTitle.trim()) {
      return;
    }

    try {
      await addTask({
        title: newTaskTitle,
        description: newTaskDescription
      });
      setNewTaskTitle('');
      setNewTaskDescription('');
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

  const startEditingTask = (task: any) => {
    setEditingTaskId(task.id);
    setEditingTaskTitle(task.title);
    setEditingTaskDescription(task.description || '');
  };

  const saveEditedTask = async (id: string) => {
    try {
      await updateTask(id, { title: editingTaskTitle, description: editingTaskDescription });
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
            <div className="bg-white overflow-hidden shadow rounded-lg p-6">
              <form onSubmit={handleAddTask} className="space-y-4">
                <div>
                  <label htmlFor="task-title" className="block text-sm font-medium text-gray-700">
                    Task Title
                  </label>
                  <input
                    type="text"
                    id="task-title"
                    value={newTaskTitle}
                    onChange={(e) => setNewTaskTitle(e.target.value)}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    placeholder="What needs to be done?"
                    required
                  />
                </div>

                <div>
                  <label htmlFor="task-description" className="block text-sm font-medium text-gray-700">
                    Description
                  </label>
                  <textarea
                    id="task-description"
                    value={newTaskDescription}
                    onChange={(e) => setNewTaskDescription(e.target.value)}
                    rows={3}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    placeholder="Add details about the task..."
                  />
                </div>

                <div>
                  <button
                    type="submit"
                    disabled={tasksLoading}
                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                  >
                    {tasksLoading ? 'Adding...' : 'Add Task'}
                  </button>
                </div>
              </form>
            </div>

            {/* Task List */}
            <div className="bg-white shadow overflow-hidden rounded-md">
              {tasksLoading ? (
                <div className="p-8 text-center">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mx-auto"></div>
                  <p className="mt-2 text-gray-600">Loading tasks...</p>
                </div>
              ) : error ? (
                <div className="p-8 text-center">
                  <div className="text-red-600">{error}</div>
                </div>
              ) : tasks.length === 0 ? (
                <div className="p-8 text-center">
                  <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                  <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
                  <p className="mt-1 text-sm text-gray-500">Get started by creating a new task.</p>
                </div>
              ) : (
                <ul className="divide-y divide-gray-200">
                  {tasks.map((task) => (
                    <li key={task.id} className="px-4 py-4 sm:px-6">
                      {editingTaskId === task.id ? (
                        // Edit mode
                        <div className="flex flex-col space-y-3">
                          <input
                            type="text"
                            value={editingTaskTitle}
                            onChange={(e) => setEditingTaskTitle(e.target.value)}
                            className="text-sm font-medium border rounded px-2 py-1 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                            autoFocus
                          />
                          <textarea
                            value={editingTaskDescription}
                            onChange={(e) => setEditingTaskDescription(e.target.value)}
                            className="text-sm border rounded px-2 py-1 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                            rows={2}
                          />
                          <div className="flex space-x-2">
                            <button
                              onClick={() => saveEditedTask(task.id)}
                              className="text-sm text-green-600 hover:text-green-800 font-medium"
                            >
                              Save
                            </button>
                            <button
                              onClick={cancelEditingTask}
                              className="text-sm text-gray-500 hover:text-gray-700 font-medium"
                            >
                              Cancel
                            </button>
                          </div>
                        </div>
                      ) : (
                        // View mode
                        <div className="flex items-center justify-between">
                          <div className="flex items-center">
                            <input
                              type="checkbox"
                              checked={task.completed}
                              onClick={() => {
                                handleToggleTask(task.id);
                              }}
                              className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                            />
                            <div className="ml-3 flex flex-col">
                              <span className={`text-sm font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                                {task.title}
                              </span>
                              {task.description && (
                                <span className={`text-sm ${task.completed ? 'line-through text-gray-400' : 'text-gray-500'}`}>
                                  {task.description}
                                </span>
                              )}
                              <span className="text-xs text-gray-400 mt-1">
                                Created: {new Date(task.created_at).toLocaleDateString()}
                              </span>
                            </div>
                          </div>
                          <div className="flex space-x-2">
                            <button
                              onClick={() => startEditingTask(task)}
                              className="text-indigo-600 hover:text-indigo-900 text-sm font-medium"
                            >
                              Edit
                            </button>
                            <button
                              onClick={() => handleDeleteTask(task.id)}
                              className="text-red-600 hover:text-red-900 text-sm font-medium"
                            >
                              Delete
                            </button>
                          </div>
                        </div>
                      )}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TasksPage;