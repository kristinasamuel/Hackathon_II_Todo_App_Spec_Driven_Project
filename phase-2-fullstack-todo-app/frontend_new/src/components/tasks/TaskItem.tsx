'use client';

import React, { useState } from 'react';
import { Task, UpdateTask } from '@/services/tasks';

interface TaskItemProps {
  task: Task;
  onToggleComplete: (id: string) => void;
  onUpdate: (id: string, data: UpdateTask) => void;
  onDelete: (id: string) => void;
  loading?: boolean;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onToggleComplete, onUpdate, onDelete, loading }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description);

  const handleSaveEdit = () => {
    onUpdate(task.id, { title: editTitle, description: editDescription });
    setIsEditing(false);
  };

  const handleCancelEdit = () => {
    setEditTitle(task.title);
    setEditDescription(task.description);
    setIsEditing(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      handleCancelEdit();
    } else if (e.key === 'Enter' && e.ctrlKey) {
      handleSaveEdit();
    }
  };

  return (
    <li className="bg-white shadow overflow-hidden rounded-md mb-2">
      {isEditing ? (
        <div className="px-4 py-4 sm:px-6">
          <div className="flex items-center justify-between">
            <div className="flex-1 min-w-0">
              <input
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                onKeyDown={handleKeyDown}
                className="font-medium text-gray-900 w-full p-1 border-b border-gray-300 focus:outline-none focus:border-indigo-500"
                autoFocus
              />
              <div className="mt-2">
                <textarea
                  value={editDescription}
                  onChange={(e) => setEditDescription(e.target.value)}
                  onKeyDown={handleKeyDown}
                  className="text-sm text-gray-500 w-full p-1 border-b border-gray-300 focus:outline-none focus:border-indigo-500"
                  rows={2}
                />
              </div>
            </div>
          </div>
          <div className="mt-3 flex justify-end space-x-2">
            <button
              onClick={handleCancelEdit}
              disabled={loading}
              className="inline-flex items-center px-3 py-1 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              Cancel
            </button>
            <button
              onClick={handleSaveEdit}
              disabled={loading}
              className="inline-flex items-center px-3 py-1 border border-transparent text-sm leading-4 font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              Save
            </button>
          </div>
        </div>
      ) : (
        <div className="px-4 py-4 sm:px-6">
          <div className="flex items-center justify-between">
            <div className="flex-1 min-w-0">
              <p className={`text-sm font-medium truncate ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                {task.title}
              </p>
              <p className={`text-sm ${task.completed ? 'line-through text-gray-400' : 'text-gray-500'} mt-1`}>
                {task.description}
              </p>
              <div className="mt-2 flex items-center">
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  {new Date(task.created_at).toLocaleDateString()}
                </span>
              </div>
            </div>
            <div className="ml-4 flex-shrink-0 flex space-x-2">
              <button
                onClick={() => onToggleComplete(task.id)}
                disabled={loading}
                className={`relative inline-flex items-center px-3 py-1 border border-transparent text-sm leading-4 font-medium rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 ${
                  task.completed
                    ? 'text-white bg-green-600 hover:bg-green-700 focus:ring-green-500'
                    : 'text-white bg-yellow-600 hover:bg-yellow-700 focus:ring-yellow-500'
                } disabled:opacity-50`}
              >
                {task.completed ? 'Completed' : 'Mark Complete'}
              </button>
              <button
                onClick={() => setIsEditing(true)}
                disabled={loading}
                className="inline-flex items-center px-3 py-1 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                Edit
              </button>
              <button
                onClick={() => onDelete(task.id)}
                disabled={loading}
                className="inline-flex items-center px-3 py-1 border border-transparent text-sm leading-4 font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </li>
  );
};

export default TaskItem;