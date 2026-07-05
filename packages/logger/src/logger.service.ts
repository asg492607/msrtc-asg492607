import { ConsoleLogger, Injectable, Scope } from '@nestjs/common';

@Injectable({ scope: Scope.TRANSIENT })
export class StructuredLogger extends ConsoleLogger {
  log(message: any, context?: string) {
    this.printLog('INFO', message, context);
  }

  error(message: any, trace?: string, context?: string) {
    this.printLog('ERROR', message, context, trace);
  }

  warn(message: any, context?: string) {
    this.printLog('WARN', message, context);
  }

  private printLog(level: string, message: any, context?: string, trace?: string) {
    const logObj = {
      timestamp: new Date().toISOString(),
      level,
      context: context || this.context,
      message,
      trace,
    };
    // In production, this output is piped into Loki/FluentBit
    console.log(JSON.stringify(logObj));
  }
}
