// Configurations for the frontend, loaded from environment variables in build time

export type Config = {
  apiHost: string;
  withoutAuthMode: boolean;
};

export function getConfig(): Config {
  const apiHost = import.meta.env.VITE_API_HOST;
  const withoutAuthMode = import.meta.env.VITE_WITHOUT_AUTH_MODE === 'true';

  if (!apiHost) {
    throw new Error('VITE_API_HOST is not set');
  }

  return {
    apiHost,
    withoutAuthMode,
  };
}
