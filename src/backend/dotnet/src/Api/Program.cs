using Appication.Query;
using Domain.repositoreis;
using EcommerceSystem.Application.Commands;
using EcommerceSystem.Domain.Events;
using EcommerceSystem.Infrastructure;
using EcommerceSystem.Infrastructure.EventBus;
using EcommerceSystem.Infrastructure.Repositories;
using MassTransit;
using Microsoft.AspNetCore.Builder;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Internal;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Serilog;
using System;
using System.Linq;
using System.Net.Mime;
using System.Text;
using System.Text.Json;

var builder = WebApplication.CreateBuilder(args);

Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Debug()
    .WriteTo.Console()
    .CreateLogger();

builder.Services.AddControllers();

// DbContext
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("Postgres")));

// Handlers e Repositories
builder.Services.AddScoped<IProductRepository, ProductRepository>();
builder.Services.AddTransient<ReserveStockCommandHandler>();
builder.Services.AddTransient<GetAllProductQueryHandler>();


// MassTransit + RabbitMQ
builder.Services.AddMassTransit(x =>
{ 
    x.AddConsumer<OrderCreatedConsumer>();

    x.UsingRabbitMq((context, cfg) =>
    {     
        cfg.Host(new Uri("amqp://guest:guest@localhost:5672/"));

        cfg.ClearMessageDeserializers();
        cfg.UseRawJsonSerializer(RawSerializerOptions.All);        
        cfg.Durable = true;
        cfg.AutoDelete = true;

        cfg.Message<StockReservedEvent>(m =>
        {          
            m.SetEntityName("ecommerce_exchange"); // nome da exchange
        });

        cfg.Publish<StockReservedEvent>(p =>
        {
            p.ExchangeType = "topic";            
        });

        cfg.ReceiveEndpoint("stock_queue", e =>
        {                                 
            e.Bind("ecommerce_exchange", s =>
            {
                s.RoutingKey = "order.created";
                s.ExchangeType = "topic";                                
            });
            e.UseRawJsonSerializer();
            e.ConfigureConsumer<OrderCreatedConsumer>(context);
        });
    });
});

// CORS
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

// Swagger
builder.Services.AddSwaggerGen();

var app = builder.Build();

app.UseCors();
app.UseSwagger();
app.UseSwaggerUI();
app.UseRouting();
app.MapControllers();
app.Run();
