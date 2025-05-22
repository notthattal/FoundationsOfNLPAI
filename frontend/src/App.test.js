import { render, screen, fireEvent } from "@testing-library/react";
import App from "./App";
import axios from "axios";

jest.mock("axios");

test("renders chat interface", () => {
  render(<App />);
  expect(screen.getByPlaceholderText("Type a message...")).toBeInTheDocument();
  expect(screen.getByText("Chat with AI")).toBeInTheDocument();
});

test("displays user message and clears input", () => {
  render(<App />);
  const input = screen.getByPlaceholderText("Type a message...");
  const button = screen.getByText("Send");

  fireEvent.change(input, { target: { value: "Hello" } });
  fireEvent.click(button);

  expect(screen.getByText("Hello")).toBeInTheDocument();
  expect(input.value).toBe("");
});

test("displays error on API failure", async () => {
  axios.post.mockRejectedValue(new Error("Network Error"));

  render(<App />);

  const input = screen.getByPlaceholderText("Type a message...");
  const button = screen.getByText("Send");

  fireEvent.change(input, { target: { value: "Test error" } });
  fireEvent.click(button);

  expect(await screen.findByText("Unable to connect to the server. Please try again.")).toBeInTheDocument();
});