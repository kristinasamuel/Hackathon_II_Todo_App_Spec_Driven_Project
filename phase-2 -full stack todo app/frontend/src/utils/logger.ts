/**
 * Comprehensive error logging utility for the Todo App frontend
 */

interface LogEntry {
  timestamp: string;
  level: 'info' | 'warn' | 'error' | 'debug';
  message: string;
  context?: any;
  user_id?: string;
  session_id?: string;
}

class Logger {
  private static readonly LOG_LEVELS = {
    DEBUG: 0,
    INFO: 1,
    WARN: 2,
    ERROR: 3
  };

  private static currentLogLevel = 'INFO';
  private sessionId: string;

  constructor() {
    // Generate a session ID for tracking related logs
    this.sessionId = this.generateSessionId();
  }

  private generateSessionId(): string {
    return 'sess_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
  }

  private shouldLog(level: keyof typeof Logger['LOG_LEVELS']): boolean {
    const currentLevel = Logger.LOG_LEVELS[Logger.currentLogLevel as keyof typeof Logger.LOG_LEVELS];
    const targetLevel = Logger.LOG_LEVELS[level];
    return targetLevel >= currentLevel;
  }

  private formatLog(entry: LogEntry): string {
    return `[${entry.timestamp}] [${entry.level.toUpperCase()}] [Session: ${entry.session_id}] - ${entry.message}${entry.context ? ` | Context: ${JSON.stringify(entry.context)}` : ''}`;
  }

  private logToConsole(entry: LogEntry): void {
    const formattedLog = this.formatLog(entry);

    switch (entry.level) {
      case 'error':
        console.error(formattedLog);
        break;
      case 'warn':
        console.warn(formattedLog);
        break;
      case 'info':
        console.info(formattedLog);
        break;
      case 'debug':
        console.debug(formattedLog);
        break;
      default:
        console.log(formattedLog);
    }
  }

  private async logToRemote(entry: LogEntry): Promise<void> {
    // In a real application, this would send logs to a remote logging service
    // For now, we'll just log to console as a placeholder
    try {
      // This is a placeholder - in production, send to a logging service like Sentry, LogRocket, etc.
      // await fetch('/api/logs', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(entry)
      // });
    } catch (error) {
      // Don't let logging errors break the application
      console.warn('Failed to send log to remote service:', error);
    }
  }

  info(message: string, context?: any): void {
    if (this.shouldLog('INFO')) {
      const entry: LogEntry = {
        timestamp: new Date().toISOString(),
        level: 'info',
        message,
        context,
        session_id: this.sessionId
      };

      this.logToConsole(entry);
      this.logToRemote(entry);
    }
  }

  warn(message: string, context?: any): void {
    if (this.shouldLog('WARN')) {
      const entry: LogEntry = {
        timestamp: new Date().toISOString(),
        level: 'warn',
        message,
        context,
        session_id: this.sessionId
      };

      this.logToConsole(entry);
      this.logToRemote(entry);
    }
  }

  error(message: string, context?: any, error?: Error): void {
    if (this.shouldLog('ERROR')) {
      const entry: LogEntry = {
        timestamp: new Date().toISOString(),
        level: 'error',
        message,
        context: {
          ...context,
          ...(error && {
            error_message: error.message,
            error_stack: error.stack,
            error_name: error.name
          })
        },
        session_id: this.sessionId
      };

      this.logToConsole(entry);
      this.logToRemote(entry);
    }
  }

  debug(message: string, context?: any): void {
    if (this.shouldLog('DEBUG')) {
      const entry: LogEntry = {
        timestamp: new Date().toISOString(),
        level: 'debug',
        message,
        context,
        session_id: this.sessionId
      };

      this.logToConsole(entry);
      this.logToRemote(entry);
    }
  }

  setLogLevel(level: keyof typeof Logger.LOG_LEVELS): void {
    if (Logger.LOG_LEVELS.hasOwnProperty(level)) {
      Logger.currentLogLevel = level;
    } else {
      console.warn(`Invalid log level: ${level}. Valid levels: ${Object.keys(Logger.LOG_LEVELS).join(', ')}`);
    }
  }
}

// Create a singleton logger instance
const logger = new Logger();
export default logger;