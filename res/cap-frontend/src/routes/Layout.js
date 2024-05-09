import { Outlet } from "react-router-dom";
import { Suspense } from "react";
import CustomLoader from "./Loader";

export default function Layout() {
  return (
    <>
      <Suspense fallback={<CustomLoader />}>
        <Outlet />
      </Suspense>
    </>
  );
}