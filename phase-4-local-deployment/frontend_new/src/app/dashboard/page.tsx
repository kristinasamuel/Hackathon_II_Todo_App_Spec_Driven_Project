'use client';

import React, { useEffect, useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useTasks } from '@/hooks/useTasks';
import { useRouter } from 'next/navigation';

const DashboardPage: React.FC = () => {
  const { user, loading: authLoading, logout, isAuthenticated } = useAuth();
  const { tasks, loading: tasksLoading, error, addTask, updateTask, deleteTask, toggleTaskCompletion, refetch } = useTasks();
  const router = useRouter();
  const [editingTaskId, setEditingTaskId] = useState<string | null>(null);
  const [editingTaskTitle, setEditingTaskTitle] = useState('');
  const [editingTaskDescription, setEditingTaskDescription] = useState('');

  useEffect(() => {
    // If user is not authenticated, redirect to login
    if (!isAuthenticated() && !authLoading) {
      router.push('/login');
    }
  }, [isAuthenticated, authLoading, router]);

  // Show loading state while checking authentication
  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 to-blue-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Checking authentication status...</p>
        </div>
      </div>
    );
  }

  // If user is not authenticated, redirect will happen in effect above
  if (!isAuthenticated()) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 to-blue-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Redirecting to login...</p>
        </div>
      </div>
    );
  }

  const handleAddTask = async (title: string, description: string) => {
    try {
      await addTask({ title, description });
    } catch (err) {
      console.error('Failed to add task:', err);
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
    try {
      await deleteTask(id);
    } catch (err) {
      console.error('Failed to delete task:', err);
    }
  };

  const handleToggleTask = async (id: string) => {
    try {
      await toggleTaskCompletion(id);
    } catch (err) {
      console.error('Failed to toggle task:', err);
    }
  };

  // Calculate task statistics
  const completedTasks = tasks.filter(task => task.completed).length;
  const totalTasks = tasks.length;
  const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-blue-100">
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {/* Dashboard Header */}
          <div className="lg:flex lg:items-center lg:justify-between mb-8">
            <div className="min-w-0 flex-1">
              <h1 className="text-3xl font-bold leading-7 text-gray-900 sm:truncate sm:text-4xl sm:tracking-tight">
                Dashboard
              </h1>
              <p className="mt-2 text-gray-600">Welcome back, {user?.name || user?.email}!</p>
            </div>
          </div>

          {/* Task Statistics Cards */}
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="px-4 py-5 sm:p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0 bg-indigo-100 rounded-md p-3">
                    <svg className="h-6 w-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Total Tasks</dt>
                      <dd className="flex items-baseline">
                        <div className="text-2xl font-semibold text-gray-900">{totalTasks}</div>
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="px-4 py-5 sm:p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0 bg-green-100 rounded-md p-3">
                    <svg className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Completed</dt>
                      <dd className="flex items-baseline">
                        <div className="text-2xl font-semibold text-gray-900">{completedTasks}</div>
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="px-4 py-5 sm:p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0 bg-yellow-100 rounded-md p-3">
                    <svg className="h-6 w-6 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Pending</dt>
                      <dd className="flex items-baseline">
                        <div className="text-2xl font-semibold text-gray-900">{totalTasks - completedTasks}</div>
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="px-4 py-5 sm:p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0 bg-blue-100 rounded-md p-3">
                    <svg className="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Completion Rate</dt>
                      <dd className="flex items-baseline">
                        <div className="text-2xl font-semibold text-gray-900">{completionRate}%</div>
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Charts Section */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
            {/* Task Distribution Chart */}
            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Task Distribution</h3>
              <div className="flex items-end h-40 gap-2 mt-8">
                <div className="flex-1 flex flex-col items-center">
                  <div
                    className="w-full bg-green-500 rounded-t"
                    style={{ height: `${completedTasks > 0 ? (completedTasks / totalTasks) * 100 : 0}%` }}
                  ></div>
                  <span className="mt-2 text-sm text-gray-600">Completed ({completedTasks})</span>
                </div>
                <div className="flex-1 flex flex-col items-center">
                  <div
                    className="w-full bg-yellow-500 rounded-t"
                    style={{ height: `${(totalTasks - completedTasks) > 0 ? ((totalTasks - completedTasks) / totalTasks) * 100 : 0}%` }}
                  ></div>
                  <span className="mt-2 text-sm text-gray-600">Pending ({totalTasks - completedTasks})</span>
                </div>
              </div>
            </div>

            {/* Completion Rate Chart */}
            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Completion Rate</h3>
              <div className="flex flex-col items-center justify-center h-40">
                <div className="relative">
                  <div className="w-32 h-32 rounded-full border-8 border-gray-200 flex items-center justify-center">
                    <div
                      className="absolute top-0 left-0 w-32 h-32 rounded-full border-8 border-transparent border-t-green-500"
                      style={{ transform: `rotate(${completionRate * 3.6}deg)` }}
                    ></div>
                    <span className="relative z-10 text-2xl font-bold text-gray-900">{completionRate}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Task List Section */}
          <div className="bg-white shadow rounded-lg overflow-hidden mb-8">
            <div className="px-6 py-5 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">My Tasks</h2>
              <p className="mt-1 text-sm text-gray-500">Manage your tasks efficiently</p>
            </div>

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
                  <li key={task.id} className="px-6 py-4">
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
                            onChange={() => {
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

          {/* Task History Section */}
          <div className="mt-8 bg-white shadow rounded-lg overflow-hidden">
            <div className="px-6 py-5 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">Task History</h2>
              <p className="mt-1 text-sm text-gray-500">Recent activity on your tasks</p>
            </div>

            <div className="p-6">
              {tasks.length === 0 ? (
                <p className="text-gray-500 text-center py-4">No task history available yet.</p>
              ) : (
                <ul className="space-y-4">
                  {tasks.slice(0, 5).map((task, index) => (
                    <li key={task.id} className="flex items-center justify-between py-3 border-b border-gray-200 last:border-0">
                      <div className="flex items-center">
                        <div className={`h-2 w-2 rounded-full mr-3 ${task.completed ? 'bg-green-500' : 'bg-yellow-500'}`}></div>
                        <div>
                          <p className="text-sm font-medium text-gray-900">{task.title}</p>
                          <p className="text-xs text-gray-500">
                            Created {new Date(task.created_at).toLocaleDateString()}
                            {task.completed && ` • Completed ${new Date(task.updated_at).toLocaleDateString()}`}
                          </p>
                        </div>
                      </div>
                      <div className="text-xs text-gray-500">
                        {task.completed ? 'Completed' : 'Pending'}
                      </div>
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

export default DashboardPage;