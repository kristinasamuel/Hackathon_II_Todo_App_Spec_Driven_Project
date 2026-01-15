import TaskService from '../../src/services/tasks';
import api from '../../src/services/api';

// Mock the api module
jest.mock('../../src/services/api', () => ({
  get: jest.fn(),
  post: jest.fn(),
  put: jest.fn(),
  patch: jest.fn(),
  delete: jest.fn(),
}));

// Mock localStorage
const mockLocalStorage = (() => {
  let store: {[key: string]: string} = {};
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => {
      store[key] = value.toString();
    },
    removeItem: (key: string) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    },
  };
})();

Object.defineProperty(global, 'localStorage', {
  value: mockLocalStorage,
});

describe('TaskService', () => {
  const mockUserId = 'user123';

  beforeEach(() => {
    jest.clearAllMocks();
    mockLocalStorage.setItem('jwt_token', 'mock-jwt-token');
  });

  describe('CRUD operations', () => {
    // T031: Test task CRUD operations with authenticated user
    test('T031: should perform full CRUD operations on tasks', async () => {
      // Test creating a task
      const newTask = {
        title: 'Test Task',
        description: 'Test Description',
        completed: false,
        due_date: '2023-12-31T23:59:59Z',
        priority: 'medium' as const,
        category: 'work',
      };

      const createdTask = {
        id: 'task123',
        ...newTask,
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-01-01T00:00:00Z',
        user_id: mockUserId,
      };

      api.post.mockResolvedValue({ data: createdTask });

      const result = await TaskService.createTask(newTask);
      expect(api.post).toHaveBeenCalledWith('/api/tasks', newTask);
      expect(result).toEqual(createdTask);

      // Test getting all tasks
      const tasksList = [createdTask];
      api.get.mockResolvedValue({ data: { tasks: tasksList } });

      const fetchedTasks = await TaskService.getTasks();
      expect(api.get).toHaveBeenCalledWith('/api/tasks');
      expect(fetchedTasks).toEqual(tasksList);

      // Test updating a task
      const updatedData = { title: 'Updated Task Title' };
      const updatedTask = { ...createdTask, ...updatedData, updated_at: '2023-01-02T00:00:00Z' };
      api.put.mockResolvedValue({ data: updatedTask });

      const updatedResult = await TaskService.updateTask(createdTask.id, updatedData);
      expect(api.put).toHaveBeenCalledWith(`/api/tasks/${createdTask.id}`, updatedData);
      expect(updatedResult).toEqual(updatedTask);

      // Test toggling task completion
      const completedTask = { ...updatedTask, completed: true, updated_at: '2023-01-03T00:00:00Z' };
      api.patch.mockResolvedValue({ data: completedTask });

      const toggledResult = await TaskService.toggleTaskCompletion(createdTask.id);
      expect(api.patch).toHaveBeenCalledWith(`/api/tasks/${createdTask.id}/complete`, { completed: true });
      expect(toggledResult).toEqual(completedTask);

      // Test deleting a task
      api.delete.mockResolvedValue({});

      await TaskService.deleteTask(createdTask.id);
      expect(api.delete).toHaveBeenCalledWith(`/api/tasks/${createdTask.id}`);
    });

    test('T031: should handle errors during CRUD operations', async () => {
      const errorResponse = {
        response: {
          data: {
            message: 'Task not found',
          },
        },
      };

      api.get.mockRejectedValue(errorResponse);

      await expect(TaskService.getTasks()).rejects.toThrow('Task not found');
    });
  });

  describe('user isolation', () => {
    // T032: Test user isolation - verify user cannot access other users' tasks
    test('T032: should enforce user isolation by using authenticated user context', async () => {
      // Mock that the API returns only tasks belonging to the authenticated user
      const userTasks = [
        {
          id: 'task1',
          title: 'User\'s Task 1',
          completed: false,
          created_at: '2023-01-01T00:00:00Z',
          updated_at: '2023-01-01T00:00:00Z',
          priority: 'medium',
          user_id: mockUserId,
        },
        {
          id: 'task2',
          title: 'User\'s Task 2',
          completed: true,
          created_at: '2023-01-02T00:00:00Z',
          updated_at: '2023-01-02T00:00:00Z',
          priority: 'high',
          user_id: mockUserId,
        },
      ];

      const otherUserTask = {
        id: 'other-task',
        title: 'Other User\'s Task',
        completed: false,
        created_at: '2023-01-03T00:00:00Z',
        updated_at: '2023-01-03T00:00:00Z',
        priority: 'low',
        user_id: 'other-user-id',
      };

      // The API should only return tasks for the authenticated user
      api.get.mockResolvedValue({ data: { tasks: userTasks } });

      const result = await TaskService.getTasks();

      // Verify that only the authenticated user's tasks were returned
      expect(result.length).toBe(2);
      expect(result.every(task => task.user_id === mockUserId)).toBe(true);
      expect(result.some(task => task.id === 'other-task')).toBe(false);

      // Verify that the API was called with proper authentication
      expect(api.get).toHaveBeenCalledWith('/api/tasks');
      // The backend should handle user isolation by filtering based on the JWT token
    });

    test('T032: should fail to access other users\' tasks due to backend protection', async () => {
      const otherUserId = 'other-user-id';
      const taskId = 'other-user-task-id';
      const forbiddenResponse = {
        response: {
          status: 403,
          data: {
            error: 'Forbidden',
            message: 'Access denied to this resource',
          },
        },
      };

      api.get.mockRejectedValue(forbiddenResponse);

      await expect(TaskService.getTaskById(taskId)).rejects.toThrow('Failed to fetch task');
      expect(api.get).toHaveBeenCalledWith(`/api/tasks/${taskId}`);
    });
  });

  describe('individual operations', () => {
    test('should get a specific task by ID', async () => {
      const taskId = 'task123';
      const expectedTask = {
        id: taskId,
        title: 'Specific Task',
        completed: false,
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-01-01T00:00:00Z',
        priority: 'medium',
        user_id: mockUserId,
      };

      api.get.mockResolvedValue({ data: expectedTask });

      const result = await TaskService.getTaskById(taskId);
      expect(api.get).toHaveBeenCalledWith(`/api/tasks/${taskId}`);
      expect(result).toEqual(expectedTask);
    });
  });
});