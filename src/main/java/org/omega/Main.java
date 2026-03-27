package org.omega;

import com.google.gson.Gson;
import org.jsoup.Connection;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

public class Main {

    public static final List<String> CATEGORIES = List.of(
            "https://dev.bg/company/jobs/back-end-development/",
            "https://dev.bg/company/jobs/front-end-development/",
            "https://dev.bg/company/jobs/full-stack-development/",
            "https://dev.bg/company/jobs/quality-assurance/",
            "https://dev.bg/company/jobs/operations/",
            "https://dev.bg/company/jobs/pm-ba-and-more/",
            "https://dev.bg/company/jobs/erp-crm-development/",
            "https://dev.bg/company/jobs/data-science/",
            "https://dev.bg/company/jobs/mobile-development/",
            "https://dev.bg/company/jobs/hardware-and-engineering/",
            "https://dev.bg/company/jobs/customer-support/",
            "https://dev.bg/company/jobs/technical-support/",
            "https://dev.bg/company/jobs/ui-ux-and-arts/");

    public static String categoryName(String categoryUrl) {
        String[] split = categoryUrl.split("/");
        String name = split[split.length-1];
        name = name.replace("-"," ");
        return name;
    }

    private record Listing(
            String category,
            String companyName,
            String position,
            String location,
            Set<String> req,
            String date,
            String url
    ){}


    public static int calculatePages(String totalListingsString){
        String[] split = totalListingsString.split(" ");
        return Math.ceilDiv(Integer.parseInt(split[0]), 20);
    }

    public static void main (String[] args) {
        CATEGORIES.forEach(Main::download);
    }

    private static void download (String startingUrl) {
        int i = 1;
        List<Listing> listings = new ArrayList<>();

        int max = 670;
        String category = categoryName(startingUrl);

        while (i != max) {
            String page = "?_paged=" + i;
            Connection connection = Jsoup.connect(startingUrl + page);
            Document document = null;
            try {
                document = connection.get();
            } catch (IOException e) {
                throw new RuntimeException(e);
            }

            if (max == 670) max = calculatePages(document.title());

            Element jobContainer = document.getElementsByClass("jobs-loop facetwp-template").getFirst();

            jobContainer.getElementsByClass("job-list-item").forEach(container -> {
                String companyName = container.getElementsByClass("company-name").getFirst().text();
                String jobName = container.getElementsByClass("job-title").getFirst().text();
                String location = container.getElementsByClass("badge").getFirst().text();
                Set<String> req = container.getElementsByClass("component-square-badge").stream()
                        .map(element -> element.getElementsByTag("img").getFirst().attr("title"))
                        .collect(Collectors.toSet());
                String date = container.getElementsByClass("date date-with-icon").getFirst().text();
                String url = container.getElementsByClass("overlay-link").attr("href");

                var listing = new Listing(category, companyName, jobName, location, req, date, url);
                System.out.println(listing);
                listings.add(listing);
            });

            i++;
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }
        listings.forEach(System.out::println);

        Gson gson = new Gson();
        String json = gson.toJson(listings);
        try {
            Files.write(Path.of("%s.json".formatted(category.replace(" ", "_"))), json.getBytes(), StandardOpenOption.CREATE);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
