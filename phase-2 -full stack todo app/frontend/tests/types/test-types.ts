// Test utility types to help with mocking
import { AxiosResponse } from 'axios';

export type MockAxiosMethod<T = any> = jest.MockedFunction<
  (url: string, data?: any, config?: any) => Promise<AxiosResponse<T>>
>;

export type MockAxiosGet = jest.MockedFunction<
  (url: string, config?: any) => Promise<AxiosResponse<any>>
>;

export type MockAxiosDelete = jest.MockedFunction<
  (url: string, config?: any) => Promise<AxiosResponse<any>>
>;