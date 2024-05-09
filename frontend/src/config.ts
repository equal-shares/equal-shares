// Configurations for the frontend, loaded from environment variables in build time

export type Config = {
  apiHost: string;
};

export function getConfig(): Config {
  const apiHost = import.meta.env.VITE_API_HOST;

  if (!apiHost) {
    throw new Error('VITE_API_HOST is not set');
  }

  return {
    apiHost
  };
}
