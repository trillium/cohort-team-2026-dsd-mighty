import { act, render } from "@testing-library/react";
import { useTheme } from "next-themes";
import { ThemeProvider } from "./ThemeProvider";

function Toggle() {
  const { setTheme } = useTheme();
  return <button type="button" aria-label="dark" onClick={() => setTheme("dark")} />;
}

describe("ThemeProvider", () => {
  beforeEach(() => {
    document.documentElement.className = "";
    vi.stubGlobal("matchMedia", (query: string) => ({
      matches: false,
      media: query,
      addEventListener: () => {},
      removeEventListener: () => {},
      addListener: () => {},
      removeListener: () => {},
      onchange: null,
      dispatchEvent: () => false,
    }));
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("sets the dark class on <html> when the theme changes to dark", () => {
    const { getByRole } = render(
      <ThemeProvider>
        <Toggle />
      </ThemeProvider>,
    );

    expect(document.documentElement).not.toHaveClass("dark");
    act(() => getByRole("button").click());
    expect(document.documentElement).toHaveClass("dark");
  });
});
