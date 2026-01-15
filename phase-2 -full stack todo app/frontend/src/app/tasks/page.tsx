'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import TaskList from '@/components/tasks/TaskList';
import ProtectedRoute from '@/components/common/ProtectedRoute';
import authService from '@/services/auth';

const TasksPage = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const authStatus = await authService.validateToken();
        setIsAuthenticated(authStatus.valid);
      } catch (error) {
        console.error('Auth check failed:', error);
        setIsAuthenticated(false);
      }
    };

    checkAuth();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">TaskManager Pro Tasks</h1>
        </div>

        {isAuthenticated ? (
          <ProtectedRoute>
            <div className="bg-white shadow rounded-lg p-6">
              <TaskList />
            </div>
          </ProtectedRoute>
        ) : (
          <div className="bg-white shadow rounded-lg p-6">
            <div className="text-center py-12">
              <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              <h3 className="mt-2 text-sm font-medium text-gray-900">Not authenticated</h3>
              <p className="mt-1 text-sm text-gray-500">Please log in to view and manage your tasks.</p>
              <div className="mt-6">
                <Link
                  href="/login"
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Sign in to your account
                </Link>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default TasksPage;