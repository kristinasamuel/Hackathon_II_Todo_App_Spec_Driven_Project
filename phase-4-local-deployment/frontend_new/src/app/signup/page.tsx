'use client';

import React, { useEffect } from 'react';
import SignupForm from '@/components/auth/SignupForm';
import { useAuth } from '@/hooks/useAuth';
import { useRouter } from 'next/navigation';

const SignupPage: React.FC = () => {
  const { user, loading, error, register, isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // If user is already authenticated, redirect to dashboard
    if (isAuthenticated()) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Checking authentication status...</p>
        </div>
      </div>
    );
  }

  // If user is already authenticated, don't show the signup form
  if (isAuthenticated()) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Redirecting to dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      <SignupForm
        onRegister={register}
        loading={loading}
        error={error}
      />
    </div>
  );
};

export default SignupPage;